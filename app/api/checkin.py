from __future__ import annotations

from fastapi import APIRouter, HTTPException
from beanie.exceptions import CollectionWasNotInitialized
from app.utils.mongodb import MongoDB
from app.schemas.checkin import CheckInRequest, CheckInResponse
from app.documents.session import Session
from app.documents.attendance import AttendanceLog
from app.utils.ws_broadcast import WSManager
import asyncio
from app.utils.totp import validate_sliding_window

router = APIRouter()


@router.post(
    "/check-in",
    response_model=CheckInResponse,
    tags=["Check-in"],
    summary="Validate a check-in attempt",
    description=(
        "Validate a student's check-in attempt using one of the supported methods: "
        "QR, BLE, Selfie, or simulated methods (NFC, Kiosk, Remote)."
    ),
)
async def validate_check_in(payload: CheckInRequest) -> CheckInResponse:
    # Fetch session
    # Retrieve session from fallback store if available to avoid Pydantic ID validation issues
    session = MongoDB.get_fallback_session(payload.session_id)
    if session is None:
        try:
            session = await Session.get(payload.session_id)
        except CollectionWasNotInitialized:
            # If the DB is not initialized and no fallback exists, session not found
            raise HTTPException(status_code=404, detail="Session not found")
        except Exception:
            # Any parsing or validation error indicates the session id wasn't valid for the DB
            raise HTTPException(status_code=404, detail="Session not found")
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    # If session inactive return error
    if (isinstance(session, dict) and not session.get("is_active", True)) or (
        not isinstance(session, dict) and not session.is_active
    ):
        # still log the attempt
        try:
            attendance_doc = AttendanceLog(
                student_id=payload.student_id,
                session_id=payload.session_id,
                method=payload.method or "QR",
                duration_ms=payload.duration_ms or 0,
                success=False,
                hci_events=payload.hci_events,
            )
            await attendance_doc.insert()
        except CollectionWasNotInitialized:
            MongoDB.add_fallback_log({
                "student_id": payload.student_id,
                "session_id": payload.session_id,
                "method": payload.method or "QR",
                "duration_ms": payload.duration_ms or 0,
                "success": False,
                "hci_events": payload.hci_events,
            })
        return CheckInResponse(success=False, reason="Session is not active")

    # Determine validation based on requested method
    strict = (payload.mode or "strict").lower() == "strict"
    required_len = 3 if strict else 1

    def _get_session_attr(s, name, default=None):
        return s.get(name, default) if isinstance(s, dict) else getattr(s, name, default)

    method = (payload.method or "QR").upper()
    is_valid = False

    if method == "QR":
        if not payload.scanned_codes:
            return CheckInResponse(success=False, reason="No codes scanned")
        is_valid = validate_sliding_window(payload.scanned_codes, _get_session_attr(session, "session_secret"), required_len=required_len)
    elif method == "BLE":
        # Use rssi threshold to accept checks; sensors use negative dBm values
        if payload.rssi is None:
            return CheckInResponse(success=False, reason="Missing RSSI")
        # Accept fairly weak signals down to -95 dBm for this prototype
        is_valid = payload.rssi > -95
    elif method == "SELFIE":
        if payload.face_detected is None:
            return CheckInResponse(success=False, reason="Missing face detection result")
        # Trust the client's liveness detection for the prototype
        is_valid = bool(payload.face_detected)
    else:
        # NFC, Kiosk, Remote and other baseline simulations are auto-accepted
        is_valid = True

    # Simple replay protection
    checked_in_students = (
        session.get("checked_in_students", [])
        if isinstance(session, dict)
        else (session.checked_in_students or [])
    )
    if is_valid and payload.student_id in checked_in_students:
        try:
            await AttendanceLog(
            student_id=payload.student_id,
            session_id=payload.session_id,
            method=payload.method or "QR",
            duration_ms=payload.duration_ms or 0,
            success=False,
            hci_events=payload.hci_events,
            ).insert()
        except CollectionWasNotInitialized:
            MongoDB.add_fallback_log({
                "student_id": payload.student_id,
                "session_id": payload.session_id,
                "method": payload.method or "QR",
                "duration_ms": payload.duration_ms or 0,
                "success": False,
                "hci_events": payload.hci_events,
            })
        return CheckInResponse(success=False, reason="Already checked in")

    # Persist log
    attendance_doc = None
    try:
        attendance_doc = AttendanceLog(
            student_id=payload.student_id,
            session_id=payload.session_id,
            method=payload.method or "QR",
            duration_ms=payload.duration_ms or 0,
            success=bool(is_valid),
            selfie_image=payload.selfie_image,
            metadata=payload.metadata,
            hci_events=payload.hci_events,
        )
        await attendance_doc.insert()
    except CollectionWasNotInitialized:
        MongoDB.add_fallback_log({
            "student_id": payload.student_id,
            "session_id": payload.session_id,
            "method": payload.method or "QR",
            "duration_ms": payload.duration_ms or 0,
            "success": bool(is_valid),
            "selfie_image": payload.selfie_image,
            "metadata": payload.metadata,
            "hci_events": payload.hci_events,
        })

    # Broadcast to open websockets for the session, if present. We emit the AttendanceLog info
    # as JSON without the selfie image to avoid sending large payloads over sockets repeatedly.
    try:
        if attendance_doc is not None:
            broadcast_payload = {
                "student_id": attendance_doc.student_id,
                "method": attendance_doc.method,
                "timestamp": attendance_doc.timestamp.isoformat(),
                "success": attendance_doc.success,
                "duration_ms": attendance_doc.duration_ms,
                "metadata": attendance_doc.metadata,
                "hci_events": attendance_doc.hci_events,
            }
            asyncio.create_task(WSManager.broadcast(payload.session_id, broadcast_payload))
    except Exception:
        pass

    if is_valid:
        # Mark student as checked in
        if isinstance(session, dict):
            session.setdefault("checked_in_students", []).append(payload.student_id)
            MongoDB.add_fallback_session(payload.session_id, session)
        else:
            session.checked_in_students = (session.checked_in_students or []) + [payload.student_id]
            await session.save()
        return CheckInResponse(success=True)

    return CheckInResponse(success=False, reason="Invalid codes")

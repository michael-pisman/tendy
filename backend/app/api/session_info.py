from __future__ import annotations

from fastapi import APIRouter, HTTPException
from app.documents.session import Session
from app.schemas.session import GetSessionResponse
from beanie.exceptions import CollectionWasNotInitialized
from app.utils.mongodb import MongoDB

router = APIRouter()


@router.get("/session/{session_id}", response_model=GetSessionResponse)
async def get_session(session_id: str) -> GetSessionResponse:
    # Try fallback store first
    session = MongoDB.get_fallback_session(session_id)
    if session is None:
        try:
            s = await Session.get(session_id)
        except CollectionWasNotInitialized:
            raise HTTPException(status_code=404, detail="Session not found")
        except Exception:
            raise HTTPException(status_code=404, detail="Session not found")
        if s is None:
            raise HTTPException(status_code=404, detail="Session not found")
        session = s

    # Normalize to dict if beanie document
    if not isinstance(session, dict):
        checked = list(session.checked_in_students or [])
        return GetSessionResponse(
            session_id=str(session.id),
            class_name=session.class_name,
            instructor_id=session.instructor_id,
            is_active=session.is_active,
            beacon_uuid=session.beacon_uuid,
            checked_in_students=checked,
        )

    return GetSessionResponse(
        session_id=session_id,
        class_name=session.get("class_name", ""),
        instructor_id=session.get("instructor_id", ""),
        is_active=bool(session.get("is_active", True)),
        beacon_uuid=session.get("beacon_uuid"),
        checked_in_students=list(session.get("checked_in_students", [])),
    )

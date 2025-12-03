from __future__ import annotations

import uuid
import secrets
from fastapi import APIRouter, HTTPException
from beanie.exceptions import CollectionWasNotInitialized
from app.utils.mongodb import MongoDB
from app.schemas.session import CreateSessionRequest, CreateSessionResponse, GetSessionResponse
from app.documents.session import Session
from typing import List

router = APIRouter()


@router.get(
    "/sessions/active",
    response_model=List[GetSessionResponse],
    tags=["Sessions"],
    summary="List all active sessions",
)
async def get_active_sessions() -> List[GetSessionResponse]:
    try:
        sessions = await Session.find(Session.is_active == True).to_list()
        return [
            GetSessionResponse(
                session_id=str(s.id),
                class_name=s.class_name,
                instructor_id=s.instructor_id,
                is_active=s.is_active,
                beacon_uuid=getattr(s, "beacon_uuid", None),
                checked_in_students=s.checked_in_students or []
            ) for s in sessions
        ]
    except CollectionWasNotInitialized:
        # Fallback for in-memory
        active = []
        for sid, s in MongoDB._sessions.items():
            if s.get("is_active"):
                active.append(GetSessionResponse(
                    session_id=sid,
                    class_name=s.get("class_name", ""),
                    instructor_id=s.get("instructor_id", ""),
                    is_active=True,
                    beacon_uuid=s.get("beacon_uuid"),
                    checked_in_students=s.get("checked_in_students", [])
                ))
        return active


@router.post(
    "/session",
    response_model=CreateSessionResponse,
    tags=["Sessions"],
    summary="Create a new instructor session",
    description=(
        "Create a new session and return a `session_secret` used by instructor "
        "apps to generate rapidly-changing QR codes. The secret is returned once."
    ),
)
async def create_session(payload: CreateSessionRequest) -> CreateSessionResponse:
    session_secret = secrets.token_hex(32)
    session = None
    try:
        session = Session(
        session_secret=session_secret,
        class_name=payload.class_name,
        instructor_id=payload.instructor_id,
        is_active=True,
        beacon_uuid=payload.beacon_uuid,
        )
        await session.insert()
    except CollectionWasNotInitialized:
        # Use in-memory fallback storage if DB is not ready
        session_id = str(uuid.uuid4())
        MongoDB.add_fallback_session(session_id, {
            "session_secret": session_secret,
            "class_name": payload.class_name,
            "instructor_id": payload.instructor_id,
            "is_active": True,
            "beacon_uuid": payload.beacon_uuid,
            "checked_in_students": [],
        })
        return CreateSessionResponse(session_id=session_id, session_secret=session_secret)
    return CreateSessionResponse(session_id=str(session.id), session_secret=session_secret)

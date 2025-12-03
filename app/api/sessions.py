from __future__ import annotations

import uuid
import secrets
from fastapi import APIRouter, HTTPException
from beanie.exceptions import CollectionWasNotInitialized
from app.utils.mongodb import MongoDB
from app.schemas.session import CreateSessionRequest, CreateSessionResponse
from app.documents.session import Session

router = APIRouter()


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

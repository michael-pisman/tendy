from __future__ import annotations

from pydantic import BaseModel


class CreateSessionRequest(BaseModel):
    instructor_id: str
    class_name: str


class CreateSessionResponse(BaseModel):
    session_id: str
    session_secret: str

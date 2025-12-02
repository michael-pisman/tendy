from __future__ import annotations

from pydantic import BaseModel


class CreateSessionRequest(BaseModel):
    instructor_id: str
    class_name: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "instructor_id": "inst-123",
                "class_name": "Computer Science 101",
            }
        }
    }


class CreateSessionResponse(BaseModel):
    session_id: str
    session_secret: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "session_id": "64b3f6a3b0f24f7bbc7a8d93",
                "session_secret": "e0de...",
            }
        }
    }

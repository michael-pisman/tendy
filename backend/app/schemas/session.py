from __future__ import annotations

from pydantic import BaseModel


class CreateSessionRequest(BaseModel):
    instructor_id: str
    class_name: str
    beacon_uuid: str | None = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "instructor_id": "inst-123",
                "class_name": "Computer Science 101",
                "beacon_uuid": "2d8b6a9e-0fe7-4e09-860a-bf27730d889c",
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


class GetSessionResponse(BaseModel):
    session_id: str
    class_name: str
    instructor_id: str
    is_active: bool
    beacon_uuid: str | None = None
    checked_in_students: list[str] = []

    model_config = {
        "json_schema_extra": {
            "example": {
                "session_id": "64b3f6a3b0f24f7bbc7a8d93",
                "class_name": "Intro to HCI",
                "instructor_id": "inst-123",
                "is_active": True,
                "beacon_uuid": "2d8b6a9e-0fe7-4e09-860a-bf27730d889c",
                "checked_in_students": ["student-1", "student-2"],
            }
        }
    }

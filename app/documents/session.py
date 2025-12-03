from __future__ import annotations

from datetime import datetime, timezone
from typing import List, Optional

from beanie import Document, Indexed
from pydantic import Field


class Session(Document):
    session_secret: str
    class_name: str
    instructor_id: str
    is_active: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    beacon_uuid: Optional[str] = None
    # Simple replay protection: list of checked-in student ids
    checked_in_students: Optional[List[str]] = Field(default_factory=list)

    class Settings:
        name = "sessions"

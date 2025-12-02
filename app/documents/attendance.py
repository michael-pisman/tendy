from __future__ import annotations

from datetime import datetime, timezone

from beanie import Document
from pydantic import Field


class AttendanceLog(Document):
    student_id: str
    session_id: str
    method: str
    duration_ms: int
    success: bool
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "attendance_logs"

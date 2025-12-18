from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional
from beanie import Document
from pydantic import Field


class PresenceLog(Document):
    session_id: str
    student_id: str
    rssi: int
    device_model: Optional[str] = None
    device_os: Optional[str] = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "presence_logs"

from __future__ import annotations

from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class PresenceRequest(BaseModel):
    student_id: str
    rssi: int
    device_model: Optional[str] = None
    device_os: Optional[str] = None
    timestamp: Optional[datetime] = None


class PresenceResponse(BaseModel):
    success: bool


class PresenceLogResponse(BaseModel):
    student_id: str
    rssi: int
    device_model: Optional[str] = None
    device_os: Optional[str] = None
    timestamp: datetime


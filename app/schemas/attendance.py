from __future__ import annotations

from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class AttendanceLogResponse(BaseModel):
    student_id: str
    method: str
    timestamp: datetime
    success: bool
    duration_ms: int
    selfie_image: Optional[str] = None
    metadata: Optional[dict] = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "student_id": "student-1",
                "method": "BLE",
                "timestamp": "2023-10-27T10:00:00Z",
                "success": True,
                "duration_ms": 120,
                "metadata": {"rssi": -65, "device_model": "iPhone 14"},
            }
        }
    }

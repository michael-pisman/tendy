from __future__ import annotations

from typing import List, Optional
from pydantic import BaseModel


class CheckInRequest(BaseModel):
    student_id: str
    session_id: str
    scanned_codes: List[str]
    duration_ms: Optional[int] = None
    method: Optional[str] = "QR"
    mode: Optional[str] = "strict"  # 'strict' or 'lenient'


class CheckInResponse(BaseModel):
    success: bool
    reason: str | None = None

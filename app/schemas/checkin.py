from __future__ import annotations

from typing import List, Optional
from pydantic import BaseModel


class CheckInRequest(BaseModel):
    student_id: str
    session_id: str
    method: str = "QR"  # QR, BLE, Selfie, NFC, Kiosk, Remote
    duration_ms: Optional[int] = 0

    # Method-specific proofs (optional)
    scanned_codes: Optional[List[str]] = None  # For QR
    rssi: Optional[int] = None                 # For BLE (negative dBm values)
    face_detected: Optional[bool] = None       # For Selfie
    mode: Optional[str] = "strict"  # 'strict' or 'lenient' only applies to QR


class CheckInResponse(BaseModel):
    success: bool
    reason: str | None = None

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
    selfie_image: Optional[str] = None         # Base64 encoded image
    mode: Optional[str] = "strict"  # 'strict' or 'lenient' only applies to QR

    model_config = {
        "json_schema_extra": {
            "examples": {
                "qr_strict": {
                    "summary": "QR strict mode",
                    "value": {
                        "student_id": "student-abc",
                        "session_id": "<session-id>",
                        "method": "QR",
                        "scanned_codes": ["code1", "code2", "code3"],
                        "mode": "strict",
                        "duration_ms": 3500,
                    },
                },
                "ble": {
                    "summary": "BLE check-in",
                    "value": {
                        "student_id": "student-ble",
                        "session_id": "<session-id>",
                        "method": "BLE",
                        "rssi": -60,
                        "duration_ms": 50,
                    },
                },
                "selfie": {
                    "summary": "Selfie check-in",
                    "value": {
                        "student_id": "student-selfie",
                        "session_id": "<session-id>",
                        "method": "Selfie",
                        "face_detected": True,
                        "duration_ms": 2100,
                    },
                },
            }
        }
    }


class CheckInResponse(BaseModel):
    success: bool
    reason: str | None = None

    model_config = {"json_schema_extra": {"example": {"success": True}}}

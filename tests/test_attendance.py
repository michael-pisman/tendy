from typing import AsyncGenerator
import pytest

from app.utils.totp import code_for_time, current_time_step


async def test_create_and_check_in(client_test: AsyncGenerator) -> None:
    # Create session
    payload = {"instructor_id": "inst-1", "class_name": "Test101"}
    resp = await client_test.post("/session", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    session_id = data["session_id"]
    secret = data["session_secret"]

    # Build codes corresponding to t-2, t-1, t to avoid codes from future time steps
    t = current_time_step()
    codes = [code_for_time(secret, t - 2 + i) for i in range(3)]

    checkin_payload = {
        "student_id": "student-abc",
        "session_id": session_id,
        "scanned_codes": codes,
        "duration_ms": 6000,
        "method": "QR",
        "mode": "strict",
    }
    resp = await client_test.post("/check-in", json=checkin_payload)
    assert resp.status_code == 200
    assert resp.json().get("success") is True

    # Repeat check-in -> should be rejected (already checked in)
    resp = await client_test.post("/check-in", json=checkin_payload)
    assert resp.status_code == 200
    assert resp.json().get("success") is False
    assert resp.json().get("reason") == "Already checked in"

    # Lenient mode with a single (valid) code should succeed for new student
    codes_single = [code_for_time(secret, t - 1)]
    checkin_payload2 = {**checkin_payload, "student_id": "student-xyz", "scanned_codes": codes_single, "mode": "lenient"}
    resp = await client_test.post("/check-in", json=checkin_payload2)
    assert resp.status_code == 200
    assert resp.json().get("success") is True

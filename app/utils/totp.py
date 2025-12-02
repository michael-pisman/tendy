from __future__ import annotations

import hmac
import hashlib
import secrets
import time
from typing import Iterable, List


def code_for_time(secret: str, t: int) -> str:
    """Generate a short deterministic code for the time step t."""
    if isinstance(secret, str):
        secret = secret.encode("utf-8")
    message = str(t).encode("utf-8")
    mac = hmac.new(secret, message, hashlib.sha256).hexdigest()
    # Truncate to keep QR compact; return lowercase
    return mac[:12]


def current_time_step(interval_seconds: int = 2) -> int:
    return int(time.time() // interval_seconds)


def codes_for_window(secret: str, window_before: int = 7, window_after: int = 0, interval_seconds: int = 2) -> List[str]:
    now = current_time_step(interval_seconds)
    codes: List[str] = []
    for dt in range(-window_before, window_after + 1):
        codes.append(code_for_time(secret, now + dt))
    return codes


def validate_sliding_window(scanned_codes: Iterable[str], secret: str, required_len: int = 3, interval_seconds: int = 2) -> bool:
    """Validate that scanned_codes contains a consecutive sequence of length `required_len` from the server-generated codes."""
    scanned = list(dict.fromkeys(scanned_codes))  # remove duplicates while preserving order
    if not scanned:
        return False
    # Generate recent valid codes
    valid_codes = codes_for_window(secret, window_before=7, window_after=0, interval_seconds=interval_seconds)
    # Check for lenient case
    if required_len <= 1:
        return any(c in valid_codes for c in scanned)
    # Build all consecutive sequences in valid_codes of length required_len and compare to windows in scanned
    for start_idx in range(0, len(valid_codes) - required_len + 1):
        seq = valid_codes[start_idx:start_idx + required_len]
        # Compare against consecutive windows in scanned list
        for i in range(0, len(scanned) - required_len + 1):
            if scanned[i:i + required_len] == seq:
                return True
    return False

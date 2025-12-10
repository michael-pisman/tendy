from __future__ import annotations

from typing import Dict, Set, Any
from fastapi import WebSocket
import asyncio


class WSManager:
    """Simple in-memory WebSocket manager to broadcast logs per session."""
    _conns: Dict[str, Set[WebSocket]] = {}

    @classmethod
    async def connect(cls, session_id: str, websocket: WebSocket) -> None:
        await websocket.accept()
        cls._conns.setdefault(session_id, set()).add(websocket)

    @classmethod
    def disconnect(cls, session_id: str, websocket: WebSocket) -> None:
        if session_id in cls._conns:
            cls._conns[session_id].discard(websocket)
            if not cls._conns[session_id]:
                cls._conns.pop(session_id, None)

    @classmethod
    async def broadcast(cls, session_id: str, payload: Any) -> None:
        """Broadcast `payload` (JSON-serializable dict) to all connections for session_id.

        Removes broken connections if sending fails.
        """
        conns = list(cls._conns.get(session_id, set()))
        if not conns:
            return
        for ws in conns:
            try:
                await ws.send_json(payload)
            except Exception:
                # Removing broken connection is safe
                try:
                    cls.disconnect(session_id, ws)
                except Exception:
                    pass

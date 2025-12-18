from fastapi import APIRouter

from app.api.sessions import router as sessions_router
from app.api.checkin import router as checkin_router
from app.api.session_info import router as session_info_router

router = APIRouter()
router.include_router(sessions_router)
router.include_router(checkin_router)
router.include_router(session_info_router)

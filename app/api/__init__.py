from fastapi import APIRouter

from app.api.sessions import router as sessions_router
from app.api.checkin import router as checkin_router

router = APIRouter()
router.include_router(sessions_router)
router.include_router(checkin_router)

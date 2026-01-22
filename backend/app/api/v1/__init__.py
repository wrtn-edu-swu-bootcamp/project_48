"""
API v1 라우트 모듈
"""
from fastapi import APIRouter
from app.api.v1 import chat, schedules, notices, programs

api_router = APIRouter()

api_router.include_router(chat.router, prefix="", tags=["chat"])
api_router.include_router(schedules.router, prefix="", tags=["schedules"])
api_router.include_router(notices.router, prefix="", tags=["notices"])
api_router.include_router(programs.router, prefix="", tags=["programs"])

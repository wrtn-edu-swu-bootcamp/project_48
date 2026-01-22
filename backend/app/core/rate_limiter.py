"""
레이트 리미팅 설정
"""
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

# 레이트 리미터 생성
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[f"{settings.API_RATE_LIMIT}/minute"],
    storage_uri=settings.REDIS_URL if settings.REDIS_ENABLED else "memory://",
    enabled=True,
)


def setup_rate_limiter(app):
    """레이트 리미터 설정"""
    app.state.limiter = limiter
    app.add_middleware(SlowAPIMiddleware)
    logger.info(f"레이트 리미팅 설정 완료: {settings.API_RATE_LIMIT}/분")
    return limiter

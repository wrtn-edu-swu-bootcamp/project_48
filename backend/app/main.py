"""
FastAPI 메인 애플리케이션 (성능 최적화)
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1 import api_router
from app.core.middleware import setup_middlewares
from app.core.rate_limiter import setup_rate_limiter
from app.core.logging_config import setup_logging
from app.core.monitoring import get_performance_monitor
import logging

# 로깅 설정
setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="서울여자대학교 신입생을 위한 AI 챗봇 서비스",
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 성능 최적화 미들웨어 설정
setup_middlewares(app)

# 레이트 리미팅 설정
limiter = setup_rate_limiter(app)

# API 라우터 등록
app.include_router(api_router)


@app.get("/")
async def root():
    """루트 엔드포인트"""
    return {
        "message": "AI 신입생 도우미 API",
        "version": settings.APP_VERSION,
    }


@app.get("/health")
async def health_check():
    """헬스 체크 엔드포인트"""
    from app.core.cache import get_cache_service
    
    cache_service = get_cache_service()
    cache_healthy = cache_service.healthcheck()
    
    return {
        "status": "healthy",
        "cache": "connected" if cache_healthy else "disconnected",
    }


@app.get("/metrics")
async def metrics():
    """성능 메트릭 조회"""
    monitor = get_performance_monitor()
    stats = monitor.get_all_stats()
    
    return {
        "status": "ok",
        "metrics": stats,
    }


@app.on_event("startup")
async def startup_event():
    """애플리케이션 시작 시 실행"""
    logger.info(f"{settings.APP_NAME} v{settings.APP_VERSION} 시작")
    logger.info(f"디버그 모드: {settings.DEBUG}")
    logger.info(f"Redis 캐싱: {'활성화' if settings.REDIS_ENABLED else '비활성화'}")


@app.on_event("shutdown")
async def shutdown_event():
    """애플리케이션 종료 시 실행"""
    logger.info(f"{settings.APP_NAME} 종료")

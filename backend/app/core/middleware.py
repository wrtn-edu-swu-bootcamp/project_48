"""
API 미들웨어 (성능 최적화)
"""
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.gzip import GZIPMiddleware
import time
import logging

logger = logging.getLogger(__name__)


class PerformanceMiddleware(BaseHTTPMiddleware):
    """성능 측정 미들웨어"""
    
    async def dispatch(self, request: Request, call_next):
        """요청 처리 시간 측정"""
        start_time = time.time()
        
        # 요청 처리
        response = await call_next(request)
        
        # 처리 시간 계산
        process_time = time.time() - start_time
        
        # 응답 헤더에 처리 시간 추가
        response.headers["X-Process-Time"] = str(process_time)
        
        # 느린 요청 로깅 (1초 이상)
        if process_time > 1.0:
            logger.warning(
                f"느린 요청 감지: {request.method} {request.url.path} - {process_time:.2f}s"
            )
        
        return response


class CacheMiddleware(BaseHTTPMiddleware):
    """캐시 헤더 추가 미들웨어"""
    
    async def dispatch(self, request: Request, call_next):
        """캐시 정책 설정"""
        response = await call_next(request)
        
        # GET 요청에 대해 캐시 헤더 추가
        if request.method == "GET":
            # API 엔드포인트별 캐시 정책
            if "/api/v1/schedules" in request.url.path:
                # 학사 일정: 1시간 캐시
                response.headers["Cache-Control"] = "public, max-age=3600"
            elif "/api/v1/notices" in request.url.path:
                # 공지사항: 5분 캐시
                response.headers["Cache-Control"] = "public, max-age=300"
            elif "/api/v1/programs" in request.url.path:
                # 지원 프로그램: 30분 캐시
                response.headers["Cache-Control"] = "public, max-age=1800"
            else:
                # 기본: 캐시 안함
                response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        
        return response


def setup_middlewares(app):
    """미들웨어 설정"""
    
    # GZIP 압축 (응답 크기 1KB 이상일 때)
    app.add_middleware(GZIPMiddleware, minimum_size=1000)
    
    # 성능 측정
    app.add_middleware(PerformanceMiddleware)
    
    # 캐시 정책
    app.add_middleware(CacheMiddleware)
    
    logger.info("미들웨어 설정 완료")

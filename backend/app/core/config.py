"""
애플리케이션 설정
"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """애플리케이션 설정"""
    
    # 애플리케이션 설정
    APP_NAME: str = "AI 신입생 도우미"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = True
    SECRET_KEY: str = ""
    
    # 데이터베이스 설정 (개발용 SQLite, 프로덕션용 PostgreSQL)
    DATABASE_URL: str = "sqlite:///./ai_freshman_helper.db"
    
    # Redis 캐싱 설정
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_ENABLED: bool = True
    CACHE_TTL_EMBEDDING: int = 86400  # 임베딩 캐시 24시간
    CACHE_TTL_SEARCH: int = 3600  # 검색 결과 캐시 1시간
    CACHE_TTL_API: int = 300  # API 응답 캐시 5분
    
    # AI API 설정
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""
    EMBEDDING_MODEL: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    
    # CORS 설정
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:3001"]
    
    # 로깅 설정
    LOG_LEVEL: str = "INFO"
    
    # 성능 설정
    MAX_WORKERS: int = 4  # 비동기 작업 워커 수
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20
    API_RATE_LIMIT: int = 100  # 분당 요청 제한
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

"""
데이터베이스 연결 설정
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# 데이터베이스 엔진 생성 (연결 풀 최적화)
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,  # 연결 유효성 체크
    pool_size=settings.DB_POOL_SIZE,  # 기본 연결 풀 크기
    max_overflow=settings.DB_MAX_OVERFLOW,  # 최대 추가 연결 수
    pool_recycle=3600,  # 1시간마다 연결 재생성
    echo=settings.DEBUG,  # 디버그 모드에서 쿼리 로깅
)

# 세션 팩토리 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 베이스 모델 클래스
Base = declarative_base()


def get_db():
    """데이터베이스 세션 의존성"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

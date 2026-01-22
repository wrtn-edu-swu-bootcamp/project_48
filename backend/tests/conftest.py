"""
Pytest configuration and fixtures for all tests.
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from app.core.database import Base, get_db
from app.main import app


# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database session for each test."""
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client with database dependency override."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def sample_question():
    """Sample user question for testing."""
    return "수강신청은 언제 하나요?"


@pytest.fixture
def sample_context():
    """Sample context for RAG testing."""
    return [
        {
            "title": "2025학년도 1학기 수강신청 안내",
            "content": "1학기 수강신청은 3월 1일부터 3월 5일까지입니다.",
            "source_type": "academic_schedule",
        }
    ]


@pytest.fixture
def mock_gemini_response():
    """Mock Gemini API response."""
    return {
        "content": [
            {
                "text": "# 수강신청 일정 안내\n\n**요약**: 1학기 수강신청은 3월 1일~5일입니다.\n\n## 상세 설명\n...\n\n**출처**: 2025학년도 학사일정"
            }
        ]
    }

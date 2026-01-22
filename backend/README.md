# Backend

Python FastAPI 기반 백엔드 서버

## 기술 스택

- Python 3.11+
- FastAPI
- SQLAlchemy (ORM)
- PostgreSQL (데이터베이스)
- OpenAI/Anthropic API (AI)

## 개발 환경 설정

### 1. 가상 환경 생성 및 활성화

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 2. 패키지 설치

```bash
pip install -r requirements.txt
```

### 3. 환경 변수 설정

`.env.example` 파일을 복사하여 `.env` 파일을 생성하고 필요한 값들을 설정하세요.

```bash
cp .env.example .env
```

### 4. 데이터베이스 설정

PostgreSQL 데이터베이스를 생성하고 `.env` 파일의 `DATABASE_URL`을 설정하세요.

### 5. 서버 실행

```bash
uvicorn app.main:app --reload
```

서버는 `http://localhost:8000`에서 실행됩니다.

API 문서는 `http://localhost:8000/docs`에서 확인할 수 있습니다.

## 프로젝트 구조

```
backend/
├── app/
│   ├── api/            # API 라우트
│   │   └── v1/        # API 버전 관리
│   ├── core/          # 핵심 설정 (config, security)
│   ├── models/        # 데이터베이스 모델
│   ├── schemas/       # Pydantic 스키마
│   ├── services/      # 비즈니스 로직
│   │   ├── ai/       # AI 서비스
│   │   ├── search/   # 검색 서비스
│   │   └── data/     # 데이터 관리 서비스
│   └── utils/         # 유틸리티 함수
├── tests/             # 테스트 코드
├── requirements.txt   # Python 패키지 목록
└── .env.example      # 환경 변수 예시
```

## 데이터베이스 마이그레이션

Alembic을 사용한 데이터베이스 마이그레이션:

```bash
# 마이그레이션 생성
alembic revision --autogenerate -m "Initial migration"

# 마이그레이션 적용
alembic upgrade head
```

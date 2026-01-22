# 로컬 실행 가이드 - 빠른 버전 (SQLite)

## 1단계: 백엔드 패키지 설치 및 환경 설정

```powershell
cd backend
pip install fastapi uvicorn anthropic sqlalchemy alembic python-dotenv pydantic-settings
```

## 2단계: .env 파일 설정

backend/.env 파일 생성 (또는 수정):
```
DATABASE_URL=sqlite:///./ai_freshman_helper.db
ANTHROPIC_API_KEY=데모용_키_입력_또는_비워두기
REDIS_ENABLED=false
```

## 3단계: 데이터베이스 초기화

```powershell
# backend 디렉토리에서
python -c "from app.core.database import Base, engine; Base.metadata.create_all(bind=engine)"
```

## 4단계: 초기 데이터 입력

```powershell
cd ..
python scripts/seed_data.py
```

## 5단계: 백엔드 실행

```powershell
cd backend
uvicorn app.main:app --reload
```

백엔드가 http://localhost:8000 에서 실행됩니다.

## 6단계: 프론트엔드 실행 (새 터미널)

```powershell
cd frontend
npm install
npm run dev
```

프론트엔드가 http://localhost:3000 에서 실행됩니다.

## 7단계: 브라우저에서 확인

- 프론트엔드: http://localhost:3000
- API 문서: http://localhost:8000/docs

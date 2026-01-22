# 🚀 AI 신입생 도우미 - 실행 가이드

## 📋 사전 준비 사항

### 1. 필수 소프트웨어 설치
- Docker Desktop (Windows/Mac) 또는 Docker Engine (Linux)
- Docker Compose V2
- Git

### 2. API 키 준비
- Anthropic Claude API 키 ([https://console.anthropic.com/](https://console.anthropic.com/))

---

## 🏃‍♂️ 빠른 시작 (Docker Compose 사용)

### 1단계: 환경 변수 설정

프로젝트 루트 디렉토리에 `.env` 파일 생성:

```bash
# env.development.example 파일 복사
cp env.development.example .env

# .env 파일 편집 - ANTHROPIC_API_KEY만 수정하면 됩니다
# ANTHROPIC_API_KEY=your_actual_api_key_here
```

**Windows PowerShell:**
```powershell
Copy-Item env.development.example .env
# 그 다음 메모장이나 에디터로 .env 파일을 열어서 API 키 수정
notepad .env
```

### 2단계: Docker Compose로 전체 시스템 실행

```bash
# 모든 서비스 시작 (백그라운드)
docker-compose up -d

# 로그 확인
docker-compose logs -f

# 특정 서비스 로그만 확인
docker-compose logs -f backend
docker-compose logs -f frontend
```

### 3단계: 초기 데이터 입력

```bash
# 백엔드 컨테이너에 접속
docker-compose exec backend bash

# 초기 데이터 입력
cd ..
python scripts/seed_data.py

# 임베딩 생성
python scripts/generate_embeddings.py

# 컨테이너 종료
exit
```

### 4단계: 애플리케이션 접속

- **프론트엔드**: http://localhost:3000
- **백엔드 API**: http://localhost:8000
- **API 문서**: http://localhost:8000/docs
- **헬스 체크**: http://localhost:8000/health

---

## 🔧 개별 서비스 실행 (로컬 개발)

Docker 없이 로컬에서 실행하려면:

### 백엔드 실행

```bash
# 1. PostgreSQL 및 Redis 설치 (별도 필요)
# PostgreSQL 14+ with pgvector extension
# Redis 7+

# 2. Python 가상환경 생성
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

# 3. 의존성 설치
pip install -r requirements.txt

# 4. 환경 변수 설정 (.env 파일 생성)
cp env.example .env
# .env 파일 편집

# 5. 데이터베이스 마이그레이션
alembic upgrade head

# 6. 초기 데이터 입력
cd ..
python scripts/seed_data.py
python scripts/generate_embeddings.py

# 7. 서버 실행
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 프론트엔드 실행

```bash
cd frontend

# 1. 의존성 설치
npm install

# 2. 환경 변수 설정
cp env.example .env.local
# .env.local 파일 편집
# NEXT_PUBLIC_API_URL=http://localhost:8000

# 3. 개발 서버 실행
npm run dev
```

---

## 🧪 테스트 실행

### 백엔드 테스트

```bash
cd backend

# 모든 테스트 실행
pytest

# 특정 테스트 파일 실행
pytest tests/test_api_chat.py

# 커버리지 포함
pytest --cov=app --cov-report=html
```

### 프론트엔드 테스트

```bash
cd frontend

# 단위 테스트 (Jest)
npm test

# E2E 테스트 (Playwright)
npm run test:e2e

# E2E UI 모드
npm run test:e2e:ui
```

---

## 🔍 상태 확인

### Docker 서비스 상태

```bash
# 실행 중인 컨테이너 확인
docker-compose ps

# 리소스 사용량 확인
docker stats

# 헬스 체크
curl http://localhost:8000/health
```

### 성능 메트릭 확인

```bash
# 백엔드 성능 메트릭
curl http://localhost:8000/metrics
```

---

## 🛑 서비스 중지

```bash
# 모든 서비스 중지
docker-compose down

# 볼륨까지 삭제 (데이터 초기화)
docker-compose down -v

# 이미지까지 삭제
docker-compose down --rmi all -v
```

---

## 🐛 문제 해결

### 포트 충돌

포트가 이미 사용 중인 경우 `.env` 파일에서 포트 변경:

```env
BACKEND_PORT=8001
FRONTEND_PORT=3001
POSTGRES_PORT=5433
REDIS_PORT=6380
```

### 데이터베이스 연결 오류

```bash
# PostgreSQL 컨테이너 로그 확인
docker-compose logs postgres

# 데이터베이스 재시작
docker-compose restart postgres

# 연결 테스트
docker-compose exec postgres psql -U postgres -d swu_chatbot
```

### Redis 연결 오류

```bash
# Redis 컨테이너 로그 확인
docker-compose logs redis

# Redis 재시작
docker-compose restart redis

# 연결 테스트
docker-compose exec redis redis-cli ping
```

### 캐시 초기화

```bash
# Redis 캐시 전체 삭제
docker-compose exec redis redis-cli FLUSHALL
```

### 로그 확인

```bash
# 모든 서비스 로그
docker-compose logs

# 실시간 로그 (tail)
docker-compose logs -f

# 최근 100줄만
docker-compose logs --tail=100

# 백엔드 애플리케이션 로그 (컨테이너 내부)
docker-compose exec backend cat /app/logs/app.log
docker-compose exec backend cat /app/logs/error.log
```

---

## 📊 개발 워크플로우

### 1. 코드 변경 후 즉시 반영 (Hot Reload)

Docker Compose 개발 환경은 코드 핫 리로드를 지원합니다:

- **백엔드**: `backend/app` 디렉토리의 Python 파일 변경 시 자동 재시작
- **프론트엔드**: `frontend/app`, `frontend/components` 디렉토리 변경 시 자동 리로드

### 2. 데이터베이스 스키마 변경

```bash
# 1. 모델 파일 수정 (backend/app/models/*.py)

# 2. 마이그레이션 생성
docker-compose exec backend alembic revision --autogenerate -m "설명"

# 3. 마이그레이션 적용
docker-compose exec backend alembic upgrade head
```

### 3. 데이터 재입력

```bash
# 전체 데이터 재입력
docker-compose exec backend bash -c "cd .. && python scripts/seed_data.py && python scripts/generate_embeddings.py"
```

---

## 🎯 다음 단계

시스템이 정상적으로 실행되면:

1. **채팅 테스트**: http://localhost:3000에서 질문 입력
2. **API 테스트**: http://localhost:8000/docs에서 Swagger UI로 API 테스트
3. **로그 모니터링**: `docker-compose logs -f` 명령으로 실시간 로그 확인
4. **성능 확인**: http://localhost:8000/metrics에서 성능 메트릭 확인

---

## 📞 지원

문제가 발생하면:

1. 로그 확인: `docker-compose logs`
2. 헬스 체크: `curl http://localhost:8000/health`
3. 컨테이너 상태: `docker-compose ps`
4. GitHub Issues에 문제 보고

---

**Happy Coding! 🎉**

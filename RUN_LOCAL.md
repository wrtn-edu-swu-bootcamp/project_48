# 🎯 Docker 없이 로컬에서 실행하기

Docker가 설치되어 있지 않은 경우, 로컬 환경에서 직접 실행할 수 있습니다.

---

## 📋 사전 준비 사항

### 1. 필수 소프트웨어 설치

#### Python (백엔드)
- Python 3.11 이상
- pip

#### Node.js (프론트엔드)
- Node.js 20 이상
- npm

#### PostgreSQL (데이터베이스)
- PostgreSQL 14 이상
- pgvector 확장

#### Redis (캐시)
- Redis 7 이상

### 2. API 키 준비
- Anthropic Claude API 키

---

## 🔧 설치 가이드

### Windows 환경

#### PostgreSQL 설치
1. https://www.postgresql.org/download/windows/ 에서 다운로드
2. 설치 시 pgAdmin 포함
3. pgvector 확장 설치:
   ```powershell
   # PostgreSQL bin 디렉토리에서
   psql -U postgres
   CREATE EXTENSION vector;
   ```

#### Redis 설치
1. https://github.com/microsoftarchive/redis/releases 에서 다운로드
2. Redis-x64-xxx.msi 설치
3. 서비스로 자동 시작

#### Python 설치
- https://www.python.org/downloads/ 에서 다운로드
- 설치 시 "Add Python to PATH" 체크

#### Node.js 설치
- https://nodejs.org/ 에서 LTS 버전 다운로드

---

## 🚀 실행 방법

### 1단계: 데이터베이스 설정

```powershell
# PostgreSQL 데이터베이스 생성
psql -U postgres
CREATE DATABASE swu_chatbot;
\c swu_chatbot
CREATE EXTENSION vector;
\q
```

### 2단계: 백엔드 설정 및 실행

```powershell
# backend 디렉토리로 이동
cd backend

# 가상환경 생성 및 활성화
python -m venv venv
.\venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 환경 변수 설정
Copy-Item env.example .env
# .env 파일 편집 (notepad .env)
# DATABASE_URL=postgresql://postgres:postgres@localhost:5432/swu_chatbot
# REDIS_URL=redis://localhost:6379/0
# ANTHROPIC_API_KEY=your_key_here

# 데이터베이스 마이그레이션
alembic upgrade head

# 초기 데이터 입력
cd ..
python scripts/seed_data.py

# 임베딩 생성
python scripts/generate_embeddings.py

# 백엔드 서버 실행
cd backend
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

서버가 시작되면 **이 터미널은 그대로 두고** 새 터미널을 엽니다.

### 3단계: 프론트엔드 설정 및 실행

**새 PowerShell 터미널에서:**

```powershell
# frontend 디렉토리로 이동
cd frontend

# 의존성 설치
npm install

# 환경 변수 설정
Copy-Item env.example .env.local
# .env.local 파일 편집
# NEXT_PUBLIC_API_URL=http://localhost:8000

# 개발 서버 실행
npm run dev
```

### 4단계: 브라우저에서 접속

- **프론트엔드**: http://localhost:3000
- **백엔드 API**: http://localhost:8000
- **API 문서**: http://localhost:8000/docs

---

## 📝 환경 변수 설정 예시

### backend/.env

```env
# 데이터베이스
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/swu_chatbot

# Redis
REDIS_URL=redis://localhost:6379/0

# API Keys
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# 환경
ENVIRONMENT=development
LOG_LEVEL=DEBUG

# CORS
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# 캐시 설정
CACHE_ENABLED=true
RATE_LIMIT_ENABLED=true
```

### frontend/.env.local

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NODE_ENV=development
```

---

## 🧪 테스트 질문

시스템이 실행되면 다음 질문을 테스트해보세요:

1. **학사 일정**: "중간고사 기간 알려줘"
2. **공지사항**: "장학금 신청 방법 알려줘"
3. **지원 프로그램**: "취업 지원 프로그램 있어?"
4. **학사 용어**: "전공심화과정이 뭐야?"

---

## 🛑 서비스 중지

### 백엔드 중지
- 백엔드 터미널에서 `Ctrl+C`

### 프론트엔드 중지
- 프론트엔드 터미널에서 `Ctrl+C`

### PostgreSQL/Redis 중지
- Windows 서비스에서 중지 또는 재부팅 시 자동 중지

---

## 🐛 문제 해결

### 포트 충돌
```powershell
# 8000 포트 사용 중인 프로세스 확인
netstat -ano | findstr :8000

# 3000 포트 사용 중인 프로세스 확인
netstat -ano | findstr :3000

# 프로세스 종료 (PID는 위에서 확인)
taskkill /PID <PID> /F
```

### PostgreSQL 연결 오류
```powershell
# PostgreSQL 서비스 상태 확인
Get-Service postgresql*

# 서비스 시작
Start-Service postgresql-x64-14  # 버전에 따라 다름
```

### Redis 연결 오류
```powershell
# Redis 서비스 상태 확인
Get-Service Redis

# 서비스 시작
Start-Service Redis
```

### Python 가상환경 활성화 오류
```powershell
# 실행 정책 변경 (관리자 권한 필요)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 가상환경 재활성화
.\venv\Scripts\activate
```

---

## 📊 현재 개발 상태 확인

### 백엔드 헬스 체크
```powershell
# PowerShell
Invoke-WebRequest -Uri http://localhost:8000/health | Select-Object -ExpandProperty Content

# 또는 브라우저에서
# http://localhost:8000/health
```

### API 문서
- http://localhost:8000/docs (Swagger UI)
- http://localhost:8000/redoc (ReDoc)

### 데이터베이스 확인
```powershell
psql -U postgres -d swu_chatbot
SELECT COUNT(*) FROM academic_schedules;
SELECT COUNT(*) FROM notices;
SELECT COUNT(*) FROM support_programs;
SELECT COUNT(*) FROM academic_glossary;
\q
```

---

## 💡 개발 팁

### 코드 변경 시 자동 재시작
- **백엔드**: uvicorn의 `--reload` 옵션으로 자동 재시작
- **프론트엔드**: Next.js의 Fast Refresh로 자동 새로고침

### 로그 확인
- **백엔드**: 터미널 출력 + `backend/logs/*.log` 파일
- **프론트엔드**: 터미널 출력 + 브라우저 개발자 도구

### 데이터베이스 변경
```powershell
# 모델 변경 후 마이그레이션 생성
cd backend
alembic revision --autogenerate -m "설명"
alembic upgrade head
```

---

**준비가 되었다면 위 단계를 순서대로 실행해보세요! 🎉**

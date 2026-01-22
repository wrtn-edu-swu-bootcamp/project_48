# 🚀 로컬 환경에서 실행하기 (Docker 없이)

Docker Desktop 앱을 설치하지 않고, Windows에 직접 필요한 프로그램을 설치하여 실행하는 방법입니다.

## 📋 필요한 프로그램

### 1. Python 3.11 이상 (백엔드)
### 2. Node.js 20 이상 (프론트엔드)  
### 3. PostgreSQL 14 이상 + pgvector (데이터베이스)
### 4. Redis 7 이상 (캐시)

---

## 🚀 설치 방법

### 1단계: Python 설치

1. **다운로드**: https://www.python.org/downloads/
2. 최신 Python 3.11 이상 버전 다운로드
3. 설치 시 **"Add Python to PATH"** 체크 필수 ✅
4. 설치 완료 후 확인:
   ```powershell
   python --version
   ```

### 2단계: Node.js 설치

1. **다운로드**: https://nodejs.org/
2. LTS 버전 다운로드 (현재 20.x 이상)
3. 설치 프로그램 실행 (기본 설정으로 진행)
4. 설치 완료 후 확인:
   ```powershell
   node --version
   npm --version
   ```

### 3단계: PostgreSQL 설치

1. **다운로드**: https://www.postgresql.org/download/windows/
2. 최신 PostgreSQL 14 이상 다운로드
3. 설치 시:
   - Password 설정 (기억해두기!)
   - Port: 5432 (기본값)
   - pgAdmin 포함하여 설치
4. **pgvector 확장 설치**:
   ```powershell
   # PostgreSQL 설치 후
   psql -U postgres
   ```
   PostgreSQL 접속 후:
   ```sql
   CREATE EXTENSION vector;
   ```

**또는 Chocolatey 사용 (간편)**:
```powershell
# 관리자 권한 PowerShell
choco install postgresql14
```

### 4단계: Redis 설치

**옵션 A: 공식 포트 (권장)**
1. **다운로드**: https://github.com/microsoftarchive/redis/releases
2. Redis-x64-3.0.504.msi 다운로드 및 설치
3. 서비스로 자동 시작됨

**옵션 B: Memurai (Redis 호환, Windows 최적화)**
1. **다운로드**: https://www.memurai.com/get-memurai
2. 무료 Developer Edition 다운로드
3. 설치 후 자동 실행

**옵션 C: Chocolatey 사용**:
```powershell
# 관리자 권한 PowerShell
choco install redis-64
```

---

## ✅ 설치 확인

모든 프로그램이 정상적으로 설치되었는지 확인:

```powershell
# Python 확인
python --version
# 출력: Python 3.11.x 이상

# Node.js 확인
node --version
# 출력: v20.x.x 이상

# npm 확인
npm --version
# 출력: 10.x.x 이상

# PostgreSQL 확인
psql --version
# 출력: psql (PostgreSQL) 14.x 이상

# Redis 확인 (서비스 상태)
Get-Service Redis*
# 또는
Get-Service Memurai
```

---

## 🎯 데이터베이스 초기 설정

### PostgreSQL 데이터베이스 생성

```powershell
# PostgreSQL 접속 (설치 시 설정한 비밀번호 입력)
psql -U postgres

# 데이터베이스 생성
CREATE DATABASE swu_chatbot;

# 데이터베이스 연결
\c swu_chatbot

# pgvector 확장 생성
CREATE EXTENSION vector;

# 종료
\q
```

### Redis 서비스 확인

```powershell
# Redis 서비스 상태 확인
Get-Service Redis*

# 실행 중이 아니면 시작
Start-Service Redis
```

---

## 🚀 프로젝트 실행하기

모든 프로그램 설치가 완료되면 프로젝트를 실행합니다.

### 1단계: 백엔드 설정 및 실행

**새 PowerShell 터미널 열기:**

```powershell
# 프로젝트 폴더로 이동
cd C:\Users\PC\Downloads\연습\backend

# Python 가상환경 생성
python -m venv venv

# 가상환경 활성화
.\venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 환경 변수 파일 생성
Copy-Item env.example .env

# .env 파일 편집 (ANTHROPIC_API_KEY 입력)
notepad .env
```

**.env 파일 내용 수정:**
```env
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/swu_chatbot
REDIS_URL=redis://localhost:6379/0
ANTHROPIC_API_KEY=your_anthropic_api_key_here
ENVIRONMENT=development
LOG_LEVEL=DEBUG
CORS_ORIGINS=http://localhost:3000
```

**계속 진행:**
```powershell
# 데이터베이스 마이그레이션
alembic upgrade head

# 초기 데이터 입력
cd ..
python scripts/seed_data.py

# 임베딩 생성 (2-3분 소요)
python scripts/generate_embeddings.py

# 백엔드 서버 실행
cd backend
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

백엔드 서버가 실행되면 **이 터미널은 그대로 두고** 새 터미널을 엽니다.

### 2단계: 프론트엔드 설정 및 실행

**새 PowerShell 터미널 열기:**

```powershell
# 프론트엔드 폴더로 이동
cd C:\Users\PC\Downloads\연습\frontend

# 의존성 설치
npm install

# 환경 변수 파일 생성
Copy-Item env.example .env.local

# .env.local 편집
notepad .env.local
```

**.env.local 파일 내용:**
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NODE_ENV=development
```

**프론트엔드 실행:**
```powershell
npm run dev
```

### 3단계: 브라우저에서 접속

- **프론트엔드**: http://localhost:3000
- **백엔드 API**: http://localhost:8000
- **API 문서**: http://localhost:8000/docs

---

## 🐛 문제 해결

### 문제 1: PostgreSQL 연결 오류

**해결방법**:
```powershell
# PostgreSQL 서비스 확인
Get-Service postgresql*

# 서비스 시작
Start-Service postgresql-x64-14  # 버전에 따라 다를 수 있음
```

### 문제 2: Redis 연결 오류

**해결방법**:
```powershell
# Redis 서비스 확인
Get-Service Redis*

# 서비스 시작
Start-Service Redis
```

### 문제 3: Python 가상환경 활성화 오류

**해결방법**:
```powershell
# 실행 정책 변경 (관리자 권한 PowerShell)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 가상환경 재활성화
.\venv\Scripts\activate
```

### 문제 4: 포트 충돌

**해결방법**:
```powershell
# 8000 포트 사용 중인 프로세스 확인
netstat -ano | findstr :8000

# 3000 포트 사용 중인 프로세스 확인
netstat -ano | findstr :3000

# 프로세스 종료 (PID는 위에서 확인)
taskkill /PID <PID> /F
```

---

## 🧪 테스트 질문

프로젝트가 실행되면 다음 질문들을 테스트해보세요:

### 학사 일정 관련
- "이번 학기 중간고사 기간은 언제야?"
- "방학은 언제부터야?"
- "개강일 알려줘"

### 공지사항 관련
- "장학금 신청 방법 알려줘"
- "최근 공지사항 뭐 있어?"
- "도서관 이용 안내"

### 지원 프로그램 관련
- "취업 지원 프로그램 있어?"
- "심리 상담 받을 수 있어?"
- "교환학생 프로그램 알려줘"

### 학사 용어 관련
- "전공심화과정이 뭐야?"
- "절대평가 설명해줘"
- "학점 이수제는 뭐야?"

---

## 🛑 서비스 중지

### 백엔드 중지
- 백엔드 터미널에서 `Ctrl+C`

### 프론트엔드 중지
- 프론트엔드 터미널에서 `Ctrl+C`

### 서비스 재시작
필요 시 PostgreSQL과 Redis 서비스 중지:
```powershell
Stop-Service postgresql*
Stop-Service Redis
```

---

## 🔗 유용한 링크

- **Python 공식 문서**: https://docs.python.org/
- **Node.js 공식 문서**: https://nodejs.org/docs/
- **PostgreSQL 공식 문서**: https://www.postgresql.org/docs/
- **Redis 공식 문서**: https://redis.io/docs/
- **FastAPI 문서**: https://fastapi.tiangolo.com/
- **Next.js 문서**: https://nextjs.org/docs

---

## 💡 추가 팁

### 자동 재시작
- **백엔드**: uvicorn의 `--reload` 옵션으로 코드 변경 시 자동 재시작
- **프론트엔드**: Next.js Fast Refresh로 자동 새로고침

### 로그 확인
- **백엔드**: 터미널 출력 + `backend/logs/*.log` 파일
- **프론트엔드**: 터미널 출력 + 브라우저 개발자 도구

### 데이터베이스 확인
```powershell
# PostgreSQL 접속
psql -U postgres -d swu_chatbot

# 데이터 확인
SELECT COUNT(*) FROM academic_schedules;
SELECT COUNT(*) FROM notices;
SELECT COUNT(*) FROM support_programs;
SELECT COUNT(*) FROM academic_glossary;

# 종료
\q
```

---

**모든 설치가 완료되었습니다! 🎉**

이제 http://localhost:3000 에서 AI 신입생 도우미를 사용할 수 있습니다!

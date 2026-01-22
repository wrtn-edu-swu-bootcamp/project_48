# 🚀 빠른 시작 가이드 (Quick Start Guide)

이 가이드를 따라하면 **10분 안에** 프로젝트를 실행할 수 있습니다!

## 📋 사전 준비사항

다음 프로그램이 설치되어 있어야 합니다:

- [ ] Python 3.10 이상
- [ ] Node.js 18 이상
- [ ] PostgreSQL 14 이상
- [ ] Git

## ⚡ 설치 단계 (10분)

### 1단계: PostgreSQL 설정 (2분)

```bash
# 1. 데이터베이스 생성
createdb swu_chatbot

# 2. pgvector 확장 설치
psql swu_chatbot -c "CREATE EXTENSION vector;"

# 완료 확인
psql swu_chatbot -c "\dx"
# vector가 목록에 보이면 성공!
```

### 2단계: Anthropic API 키 발급 (3분)

1. https://console.anthropic.com 방문
2. 회원가입 / 로그인
3. API Keys 메뉴에서 새 키 생성
4. 키를 복사해두기 (나중에 사용)

**무료 크레딧**: 신규 가입 시 $5 크레딧 제공 (테스트용으로 충분)

### 3단계: 백엔드 설정 (3분)

```bash
# 1. 프로젝트 디렉토리로 이동
cd backend

# 2. 가상환경 생성 (선택사항이지만 권장)
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

# 3. 패키지 설치
pip install -r requirements.txt

# 4. 환경 변수 설정
cp env.example .env

# 5. .env 파일 편집 (텍스트 에디터로)
# DATABASE_URL=postgresql://사용자명:비밀번호@localhost:5432/swu_chatbot
# ANTHROPIC_API_KEY=여기에_복사한_API_키_붙여넣기
```

**Windows 사용자 주의**: 
- PostgreSQL 기본 사용자명: `postgres`
- 비밀번호: 설치 시 입력한 것

예시:
```
DATABASE_URL=postgresql://postgres:mypassword@localhost:5432/swu_chatbot
```

### 4단계: 데이터베이스 초기화 (2분)

```bash
# 백엔드 디렉토리에서 계속

# 1. 마이그레이션 실행
alembic upgrade head

# 2. 프로젝트 루트로 이동
cd ..

# 3. 초기 데이터 입력
python scripts/seed_data.py

# 4. 임베딩 생성 (약 1-2분 소요)
python scripts/generate_embeddings.py
```

**중요**: 임베딩 생성은 처음 한 번만 실행하면 됩니다!

## 🎯 실행 (1분)

### 터미널 1: 백엔드 실행

```bash
cd backend
uvicorn app.main:app --reload
```

**성공 메시지**:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

### 터미널 2: 프론트엔드 실행

```bash
cd frontend

# 처음 한 번만
npm install

# 개발 서버 실행
npm run dev
```

**성공 메시지**:
```
ready - started server on 0.0.0.0:3000
```

## ✅ 확인

### 1. 백엔드 작동 확인

브라우저에서 http://localhost:8000/docs 접속

→ Swagger UI가 보이면 성공!

### 2. 프론트엔드 작동 확인

브라우저에서 http://localhost:3000 접속

→ 메인 페이지가 보이면 성공!

### 3. 채팅 테스트

1. http://localhost:3000/chat 접속
2. 질문 입력: "수강신청은 언제 하나요?"
3. AI 답변이 나오면 성공! 🎉

## 🐛 문제 해결

### 문제 1: pgvector 설치 실패

**증상**: `CREATE EXTENSION vector;` 실행 시 오류

**해결**:
```bash
# Ubuntu/Debian
sudo apt install postgresql-14-pgvector

# Mac (Homebrew)
brew install pgvector

# Windows
# pgvector GitHub에서 바이너리 다운로드
# https://github.com/pgvector/pgvector/releases
```

### 문제 2: 백엔드 실행 오류 - "No module named 'anthropic'"

**증상**: 패키지를 찾을 수 없다는 오류

**해결**:
```bash
# 가상환경이 활성화되어 있는지 확인
which python  # venv 경로가 나와야 함

# 패키지 재설치
pip install -r requirements.txt
```

### 문제 3: 프론트엔드 실행 오류 - "npm ERR!"

**증상**: npm install 실패

**해결**:
```bash
# Node 버전 확인
node --version  # v18 이상이어야 함

# 캐시 삭제 후 재설치
rm -rf node_modules package-lock.json
npm install
```

### 문제 4: 데이터베이스 연결 실패

**증상**: "could not connect to server"

**해결**:
```bash
# PostgreSQL 실행 상태 확인
# Mac
brew services list

# Ubuntu
sudo systemctl status postgresql

# Windows
# 서비스 관리자에서 PostgreSQL 확인

# PostgreSQL 시작
# Mac
brew services start postgresql

# Ubuntu
sudo systemctl start postgresql

# Windows
# 서비스 관리자에서 시작
```

### 문제 5: Claude API 오류 - "Authentication Error"

**증상**: API 호출 시 인증 오류

**해결**:
1. .env 파일의 ANTHROPIC_API_KEY 확인
2. API 키에 공백이나 따옴표가 없는지 확인
3. API 키가 유효한지 확인 (https://console.anthropic.com)

## 📱 첫 번째 테스트

### 테스트 질문 예시

1. **학사 일정**:
   - "수강신청은 언제 하나요?"
   - "1학기 등록금 납부 기간이 궁금해요"
   - "중간고사는 언제인가요?"

2. **지원 프로그램**:
   - "장학금 신청 방법 알려주세요"
   - "비교과 프로그램에는 뭐가 있나요?"
   - "취업 멘토링 프로그램이 궁금해요"

3. **학사 용어**:
   - "복수전공이 뭔가요?"
   - "학점제에 대해 설명해주세요"
   - "휴학은 어떻게 신청하나요?"

## 🎓 다음 단계

축하합니다! 프로젝트가 성공적으로 실행되었습니다.

### 추가 학습 자료

1. **Architecture.md**: 시스템 구조 이해
2. **Design_Guide.md**: UI/UX 디자인 시스템
3. **DEVELOPMENT_STATUS.md**: 개발 진행 상황
4. **README.md**: 전체 프로젝트 문서

### 커스터마이징

1. **데이터 추가**:
   - `scripts/data/` 폴더의 JSON 파일 편집
   - `python scripts/seed_data.py` 재실행
   - `python scripts/generate_embeddings.py` 재실행

2. **프롬프트 수정**:
   - `backend/app/services/ai/prompts.py` 편집
   - 백엔드 서버 재시작

3. **UI 커스터마이징**:
   - `frontend/app/globals.css` 에서 색상/폰트 변경
   - `frontend/components/` 에서 컴포넌트 수정

## 🆘 추가 도움이 필요하신가요?

- **문서**: README.md, IMPLEMENTATION_COMPLETE.md 참조
- **API 문서**: http://localhost:8000/docs
- **로그 확인**: 터미널 출력 확인

---

**예상 소요 시간 요약**:
- PostgreSQL 설정: 2분
- API 키 발급: 3분
- 백엔드 설정: 3분
- 데이터베이스 초기화: 2분
- 실행: 1분

**총 소요 시간**: 약 10분

**행운을 빕니다! 🚀**

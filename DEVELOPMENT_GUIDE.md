# AI 신입생 도우미 - 개발 가이드

## 프로젝트 개요

서울여자대학교 신입생을 위한 AI 기반 챗봇 시스템입니다.

**주요 기능:**
- 학사 일정 안내
- 공지사항 검색
- 지원 프로그램 안내
- 학사 용어 설명

**기술 스택:**
- **Backend**: FastAPI, Python 3.10+, PostgreSQL/SQLite, Claude AI
- **Frontend**: Next.js 14, React 18, TypeScript, Tailwind CSS
- **AI**: Anthropic Claude API, sentence-transformers (한국어 임베딩)

---

## 시작하기

### 1. 환경 요구사항

- Python 3.10 이상
- Node.js 18 이상
- PostgreSQL 14+ (프로덕션) 또는 SQLite (개발)

### 2. 백엔드 설정

#### 2.1 의존성 설치

```bash
cd backend
pip install -r requirements.txt
```

#### 2.2 환경 변수 설정

`.env` 파일을 backend 폴더에 생성하고 다음 내용을 입력하세요:

```env
# 애플리케이션 설정
APP_NAME="AI 신입생 도우미"
DEBUG=True

# 데이터베이스 (개발용 SQLite)
DATABASE_URL="sqlite:///./ai_freshman_helper.db"

# AI API 키
ANTHROPIC_API_KEY="your-api-key-here"
EMBEDDING_MODEL="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

# CORS 설정
CORS_ORIGINS=["http://localhost:3000"]
```

**중요:** Anthropic API 키를 발급받아 입력하세요:
https://console.anthropic.com/

#### 2.3 데이터베이스 초기화

```bash
# 테이블 생성
python scripts/init_db.py

# 초기 데이터 입력
python scripts/seed_data.py

# 임베딩 생성 (선택사항)
python scripts/generate_embeddings.py
```

#### 2.4 백엔드 실행

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

백엔드 서버가 `http://localhost:8000`에서 실행됩니다.

API 문서: http://localhost:8000/docs

### 3. 프론트엔드 설정

#### 3.1 의존성 설치

```bash
cd frontend
npm install
```

#### 3.2 환경 변수 설정

`.env.local` 파일을 frontend 폴더에 생성하고 다음 내용을 입력하세요:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

#### 3.3 프론트엔드 실행

```bash
cd frontend
npm run dev
```

프론트엔드가 `http://localhost:3000`에서 실행됩니다.

---

## 프로젝트 구조

```
.
├── backend/                 # FastAPI 백엔드
│   ├── app/
│   │   ├── api/v1/         # API 엔드포인트
│   │   ├── core/           # 설정 및 데이터베이스
│   │   ├── models/         # SQLAlchemy 모델
│   │   ├── schemas/        # Pydantic 스키마
│   │   └── services/       # 비즈니스 로직
│   │       └── ai/         # AI 관련 서비스
│   ├── alembic/            # 데이터베이스 마이그레이션
│   └── requirements.txt    # Python 의존성
├── frontend/               # Next.js 프론트엔드
│   ├── app/                # Next.js 13+ App Router
│   ├── components/         # React 컴포넌트
│   ├── hooks/              # React Hooks
│   ├── lib/                # 유틸리티 및 API 클라이언트
│   └── types/              # TypeScript 타입 정의
├── scripts/                # 데이터베이스 초기화 스크립트
│   └── data/               # 초기 데이터 (JSON)
└── docs/                   # 문서
    ├── Architecture.md     # 시스템 아키텍처
    ├── Design_Guide.md     # 디자인 가이드
    └── 기획안.md            # 프로젝트 기획안
```

---

## 주요 기능 구현 상태

### ✅ 완료된 기능

**백엔드:**
- [x] FastAPI 애플리케이션 설정
- [x] PostgreSQL/SQLite 데이터베이스 연동
- [x] 학사 일정, 공지사항, 지원 프로그램 모델
- [x] 벡터 검색 (pgvector) 및 하이브리드 검색
- [x] Anthropic Claude API 연동
- [x] RAG (Retrieval-Augmented Generation) 파이프라인
- [x] 질문 분류 시스템
- [x] 답변 검증 및 폴백 메커니즘
- [x] 채팅 API 엔드포인트
- [x] 학사일정/공지사항/지원프로그램 API

**프론트엔드:**
- [x] Next.js 14 App Router 설정
- [x] TypeScript 설정
- [x] Tailwind CSS 디자인 시스템
- [x] 채팅 UI 컴포넌트 (메시지, 입력, 타이핑 인디케이터)
- [x] 메인 페이지 및 채팅 페이지
- [x] API 클라이언트 및 React Hooks
- [x] 반응형 디자인 (모바일/태블릿/데스크톱)

### 🔄 개선 가능한 부분

- [ ] 사용자 인증 및 세션 관리
- [ ] 관리자 대시보드
- [ ] 피드백 시스템 고도화
- [ ] 성능 모니터링
- [ ] E2E 테스트
- [ ] Docker 컨테이너화

---

## 개발 가이드

### 코딩 컨벤션

자세한 내용은 `.cursorrules` 파일을 참고하세요.

**React:**
- 함수형 컴포넌트 사용
- TypeScript 타입 정의
- Tailwind CSS 인라인 스타일
- 접근성 (ARIA, 키보드 네비게이션) 준수

**Python:**
- Black 포맷터 사용
- Type hints 사용
- Docstring 작성
- PEP 8 준수

### 데이터 추가하기

초기 데이터는 `scripts/data/` 폴더의 JSON 파일에 있습니다:

- `academic_schedules.json`: 학사 일정
- `notices.json`: 공지사항
- `support_programs.json`: 지원 프로그램
- `glossary.json`: 학사 용어 사전

데이터를 수정한 후 다시 실행:

```bash
python scripts/seed_data.py
python scripts/generate_embeddings.py
```

---

## 문제 해결

### 백엔드 실행 오류

**오류:** `ModuleNotFoundError: No module named 'anthropic'`

**해결:** 의존성을 다시 설치하세요
```bash
pip install -r backend/requirements.txt
```

**오류:** `API key not found`

**해결:** `.env` 파일에 Anthropic API 키를 설정하세요

### 프론트엔드 실행 오류

**오류:** `Cannot connect to backend`

**해결:** 백엔드 서버가 실행 중인지 확인하세요 (http://localhost:8000/health)

**오류:** `Module not found`

**해결:** 의존성을 다시 설치하세요
```bash
cd frontend
npm install
```

---

## API 문서

백엔드 서버 실행 후 다음 URL에서 API 문서를 확인하세요:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 주요 엔드포인트

**채팅:**
- `POST /api/v1/chat` - 질문 전송 및 답변 받기

**학사일정:**
- `GET /api/v1/schedules` - 학사 일정 목록 조회
- `GET /api/v1/schedules/{id}` - 특정 일정 조회

**공지사항:**
- `GET /api/v1/notices` - 공지사항 목록 조회
- `GET /api/v1/notices/{id}` - 특정 공지 조회

**지원프로그램:**
- `GET /api/v1/programs` - 프로그램 목록 조회
- `GET /api/v1/programs/{id}` - 특정 프로그램 조회

---

## 배포

### 프로덕션 설정

**백엔드:**
1. PostgreSQL 데이터베이스 설정
2. `DATABASE_URL` 환경 변수 업데이트
3. `DEBUG=False` 설정
4. Gunicorn 또는 Uvicorn으로 프로덕션 서버 실행

**프론트엔드:**
1. `npm run build`로 프로덕션 빌드
2. `npm start`로 서버 실행
3. 또는 Vercel/Netlify에 배포

---

## 라이선스

이 프로젝트는 교육 목적으로 개발되었습니다.

---

## 문의

개발 관련 문의:
- 이슈 트래커: GitHub Issues
- 문서: `docs/` 폴더 참고

---

**마지막 업데이트:** 2026년 1월 22일

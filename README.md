# AI 신입생 도우미 (서울여자대학교)

서울여자대학교 신입생을 위한 AI 챗봇 서비스입니다.

## 주요 기능

- 학사 일정 안내 (수강신청, 등록금 납부, 휴학 등)
- 공지사항 안내
- 지원 프로그램 안내 (장학금, 비교과, 멘토링)
- 신입생 기본 정보 안내 (학사 용어, 제도 설명)

## 기술 스택

- **Frontend**: Next.js 16, React 19, Tailwind CSS 4
- **Backend**: Next.js API Routes
- **AI**: Google Gemini 2.0 Flash
- **Database**: Vercel Postgres (선택)
- **Deployment**: Vercel

## 시작하기

### 1. 의존성 설치

```bash
cd frontend
npm install
```

### 2. 환경 변수 설정

`.env.example`을 `.env.local`로 복사하고 Gemini API 키를 설정합니다.

```bash
cp .env.example .env.local
```

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

Gemini API 키는 [Google AI Studio](https://aistudio.google.com/apikey)에서 무료로 발급받을 수 있습니다.

### 3. 개발 서버 실행

```bash
npm run dev
```

http://localhost:3000 에서 확인할 수 있습니다.

## Vercel 배포

### 1. Vercel CLI 설치

```bash
npm install -g vercel
```

### 2. 로그인 및 배포

```bash
cd frontend
vercel login
vercel
```

### 3. 환경 변수 설정

Vercel 대시보드에서 다음 환경 변수를 설정합니다:

- `GEMINI_API_KEY`: Google Gemini API 키

### 4. 프로덕션 배포

```bash
vercel --prod
```

## 프로젝트 구조

```
frontend/
├── app/
│   ├── api/
│   │   ├── chat/           # 채팅 API
│   │   ├── schedules/      # 학사일정 API
│   │   ├── notices/        # 공지사항 API
│   │   └── programs/       # 지원프로그램 API
│   ├── chat/               # 채팅 페이지
│   └── layout.tsx
├── components/
│   ├── chat/               # 채팅 컴포넌트
│   ├── layout/             # 레이아웃 컴포넌트
│   └── ui/                 # UI 컴포넌트
├── hooks/
│   └── useChat.ts          # 채팅 훅
├── lib/
│   ├── api.ts              # API 클라이언트
│   ├── gemini.ts           # Gemini 클라이언트
│   └── rag.ts              # RAG 파이프라인
├── prisma/
│   └── schema.prisma       # DB 스키마 (선택)
└── vercel.json             # Vercel 설정
```

## API 엔드포인트

| 엔드포인트 | 메서드 | 설명 |
|-----------|--------|------|
| `/api/chat` | POST | 채팅 질문 처리 |
| `/api/chat/stream` | POST | 스트리밍 응답 |
| `/api/schedules` | GET | 학사 일정 조회 |
| `/api/notices` | GET | 공지사항 조회 |
| `/api/programs` | GET | 지원 프로그램 조회 |

## 라이선스

MIT License

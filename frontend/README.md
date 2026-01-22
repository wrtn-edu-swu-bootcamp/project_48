# Frontend

Next.js 기반 프론트엔드 애플리케이션

## 기술 스택

- Next.js 14+ (App Router)
- TypeScript
- Tailwind CSS
- React 18+

## 개발 환경 설정

```bash
npm install
npm run dev
```

개발 서버는 `http://localhost:3000`에서 실행됩니다.

## 프로젝트 구조

```
frontend/
├── app/                # Next.js App Router
│   ├── globals.css    # 글로벌 스타일 및 디자인 토큰
│   ├── layout.tsx    # 루트 레이아웃
│   └── page.tsx      # 홈 페이지
├── components/        # 재사용 컴포넌트
│   ├── ui/          # 기본 UI 컴포넌트
│   ├── chat/        # 챗봇 관련 컴포넌트
│   └── layout/      # 레이아웃 컴포넌트
├── hooks/           # 커스텀 훅
├── lib/             # 유틸리티 함수
├── styles/          # 추가 스타일 파일
└── types/           # TypeScript 타입 정의
```

## 디자인 시스템

디자인 토큰은 `app/globals.css`에 정의되어 있습니다. 자세한 내용은 `docs/Design_Guide.md`를 참조하세요.

## 빌드

```bash
npm run build
npm start
```

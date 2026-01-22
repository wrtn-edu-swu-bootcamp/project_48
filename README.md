# AI 신입생 도우미 🎓

서울여자대학교 신입생을 위한 AI 기반 챗봇 서비스입니다.

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-14-black.svg)](https://nextjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5-blue.svg)](https://www.typescriptlang.org/)

## ✨ 주요 기능

- 📅 **학사 일정 안내**: 수강신청, 등록금 납부, 시험 일정 등
- 📢 **공지사항 검색**: 학교 공지사항을 빠르게 확인
- 💡 **지원 프로그램 안내**: 장학금, 비교과 프로그램, 멘토링 정보
- 📖 **학사 용어 설명**: 복잡한 학사 용어를 쉽게 이해
- 🤖 **AI 기반 대화**: Claude AI를 활용한 자연스러운 대화
- 🔍 **RAG 검색**: 벡터 검색을 통한 정확한 정보 제공

## 🏗️ 기술 스택

### Backend
- **Framework**: FastAPI
- **Database**: PostgreSQL (프로덕션) / SQLite (개발)
- **AI**: Anthropic Claude API, sentence-transformers
- **Vector Search**: pgvector
- **ORM**: SQLAlchemy

### Frontend
- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **State**: React Hooks

## 🚀 빠른 시작

### 필수 요구사항

- Python 3.10 이상
- Node.js 18 이상
- Anthropic API 키 ([발급받기](https://console.anthropic.com/))

### 1. 프로젝트 클론

```bash
git clone https://github.com/yourusername/ai-freshman-helper.git
cd ai-freshman-helper
```

### 2. 백엔드 설정

```bash
cd backend

# 의존성 설치
pip install -r requirements.txt

# 환경 변수 설정
# .env 파일을 생성하고 다음을 입력:
# ANTHROPIC_API_KEY=your-api-key-here
# DATABASE_URL=sqlite:///./ai_freshman_helper.db

# 데이터베이스 초기화
python scripts/init_db.py
python scripts/seed_data.py

# 서버 실행
uvicorn app.main:app --reload
```

백엔드가 `http://localhost:8000`에서 실행됩니다.

### 3. 프론트엔드 설정

```bash
cd frontend

# 의존성 설치
npm install

# 환경 변수 설정
# .env.local 파일을 생성하고 다음을 입력:
# NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1

# 개발 서버 실행
npm run dev
```

프론트엔드가 `http://localhost:3000`에서 실행됩니다.

## 📚 문서

- [개발 가이드](./DEVELOPMENT_GUIDE.md) - 상세한 설치 및 개발 가이드
- [시스템 아키텍처](./docs/Architecture.md) - 시스템 구조 및 RAG 패턴
- [디자인 가이드](./docs/Design_Guide.md) - UI/UX 디자인 시스템
- [프로젝트 기획안](./docs/기획안.md) - 프로젝트 기획 및 요구사항
- [API 문서](http://localhost:8000/docs) - FastAPI 자동 생성 문서

## 🎯 프로젝트 구조

```
.
├── backend/              # FastAPI 백엔드
│   ├── app/
│   │   ├── api/         # API 엔드포인트
│   │   ├── models/      # 데이터베이스 모델
│   │   ├── services/    # 비즈니스 로직
│   │   │   └── ai/      # AI 서비스 (RAG, Claude)
│   │   └── schemas/     # Pydantic 스키마
│   └── scripts/         # 데이터베이스 초기화
├── frontend/            # Next.js 프론트엔드
│   ├── app/             # Next.js App Router
│   ├── components/      # React 컴포넌트
│   ├── hooks/           # Custom Hooks
│   └── lib/             # API 클라이언트
├── scripts/             # 유틸리티 스크립트
│   └── data/            # 초기 데이터 (JSON)
└── docs/                # 프로젝트 문서
```

## 🔧 개발 현황

### ✅ 구현 완료

**Phase 1: 데이터베이스 & 백엔드**
- [x] PostgreSQL/SQLite 데이터베이스 설계
- [x] 벡터 임베딩 시스템
- [x] Anthropic Claude API 연동
- [x] RAG (Retrieval-Augmented Generation) 파이프라인
- [x] 질문 분류 시스템
- [x] 하이브리드 검색 (키워드 + 벡터)

**Phase 2: API 엔드포인트**
- [x] 채팅 API
- [x] 학사일정 API
- [x] 공지사항 API
- [x] 지원프로그램 API

**Phase 3: 프론트엔드 UI**
- [x] 메인 페이지
- [x] 채팅 인터페이스
- [x] 반응형 디자인
- [x] 접근성 지원

**Phase 4: 통합 & 테스트**
- [x] 프론트엔드-백엔드 API 연동
- [x] Tailwind CSS 디자인 시스템
- [x] 에러 핸들링 및 폴백 시스템

### 🔄 향후 개선 사항

- [ ] 사용자 인증 시스템
- [ ] 관리자 대시보드
- [ ] 피드백 수집 및 분석
- [ ] 성능 모니터링
- [ ] Docker 컨테이너화
- [ ] CI/CD 파이프라인

## 🤝 기여하기

프로젝트 개선을 위한 제안이나 버그 리포트는 언제든 환영합니다!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 라이선스

이 프로젝트는 교육 목적으로 개발되었습니다.

## 📞 문의

프로젝트 관련 문의사항은 GitHub Issues를 통해 제출해주세요.

---

**개발 완료일**: 2026년 1월 22일  
**개발자**: AI Assistant with Cursor  
**대학**: 서울여자대학교

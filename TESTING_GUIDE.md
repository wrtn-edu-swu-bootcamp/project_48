# 테스트 가이드

이 문서는 AI 신입생 도우미 프로젝트의 테스트 실행 방법을 설명합니다.

## 백엔드 테스트 (Python/pytest)

### 설치
```bash
cd backend
pip install -r requirements.txt
```

### 테스트 실행

#### 모든 테스트 실행
```bash
pytest
```

#### 특정 테스트 파일만 실행
```bash
pytest tests/test_embeddings.py
```

#### 마커별 실행
```bash
# 단위 테스트만
pytest -m unit

# 통합 테스트만
pytest -m integration
```

#### 커버리지 리포트 생성
```bash
pytest --cov=app --cov-report=html
```

HTML 리포트는 `htmlcov/index.html`에서 확인할 수 있습니다.

#### 상세 출력
```bash
pytest -v
```

### 백엔드 테스트 구조
```
backend/tests/
├── conftest.py                 # 테스트 픽스처 및 설정
├── test_embeddings.py          # 임베딩 서비스 단위 테스트
├── test_search.py              # 검색 서비스 단위 테스트
├── test_validator.py           # 답변 검증기 단위 테스트
├── test_rag.py                 # RAG 파이프라인 통합 테스트
├── test_api_chat.py            # 채팅 API 통합 테스트
├── test_api_schedules.py       # 학사일정 API 통합 테스트
├── test_api_notices.py         # 공지사항 API 통합 테스트
└── test_api_programs.py        # 지원프로그램 API 통합 테스트
```

### 주요 테스트 케이스

#### 임베딩 서비스 (test_embeddings.py)
- 싱글톤 패턴 검증
- 단일 텍스트 임베딩 생성
- 배치 임베딩 생성
- 유사도 검증

#### 검색 서비스 (test_search.py)
- 키워드 기반 검색
- 4개 테이블 검색 (학사일정, 공지사항, 지원프로그램, 학사용어)
- 빈 결과 처리

#### RAG 파이프라인 (test_rag.py)
- 전체 RAG 파이프라인 흐름
- 컨텍스트 부재 시 처리
- 에러 처리
- 질문 분류

#### API 엔드포인트 (test_api_*.py)
- 정상 요청 처리
- 유효성 검증
- 에러 처리
- 필터링

---

## 프론트엔드 테스트

### 설치
```bash
cd frontend
npm install
```

### Jest 테스트 (컴포넌트 단위 테스트)

#### 모든 테스트 실행
```bash
npm test
```

#### Watch 모드 (개발 중)
```bash
npm run test:watch
```

#### 커버리지 리포트
```bash
npm run test:coverage
```

#### 특정 파일만 테스트
```bash
npm test ChatArea.test.tsx
```

### Jest 테스트 구조
```
frontend/
├── components/
│   ├── chat/__tests__/
│   │   ├── ChatArea.test.tsx
│   │   ├── InputArea.test.tsx
│   │   ├── UserMessage.test.tsx
│   │   ├── BotMessage.test.tsx
│   │   └── TypingIndicator.test.tsx
│   └── ui/__tests__/
│       └── Button.test.tsx
└── hooks/__tests__/
    └── useChat.test.ts
```

### 주요 컴포넌트 테스트

#### ChatArea
- 메시지 표시
- 타이핑 인디케이터
- 환영 메시지
- 출처 표시
- ARIA 속성

#### InputArea
- 텍스트 입력
- 전송 버튼 클릭
- Enter 키 전송
- Shift+Enter 줄바꿈
- 로딩 상태
- 빈 메시지 방지

#### useChat Hook
- 메시지 전송
- 로딩 상태 관리
- 에러 처리
- 메시지 히스토리

---

### Playwright E2E 테스트 (통합 시나리오)

#### Playwright 설치 (최초 1회)
```bash
cd frontend
npx playwright install
```

#### E2E 테스트 실행
```bash
# 헤드리스 모드 (빠름)
npm run test:e2e

# UI 모드 (디버깅용)
npm run test:e2e:ui

# 브라우저 보면서 실행
npm run test:e2e:headed
```

#### 특정 브라우저만 테스트
```bash
npx playwright test --project=chromium
npx playwright test --project=firefox
npx playwright test --project=webkit
```

#### 특정 파일만 테스트
```bash
npx playwright test chat-flow.spec.ts
```

### E2E 테스트 구조
```
frontend/e2e/
├── chat-flow.spec.ts         # 채팅 기능 시나리오
├── navigation.spec.ts        # 페이지 네비게이션
└── accessibility.spec.ts     # 접근성 테스트
```

### 주요 E2E 시나리오

#### 채팅 흐름 (chat-flow.spec.ts)
- 페이지 로드 및 UI 표시
- 환영 메시지 및 예시 질문
- 메시지 전송 및 응답 수신
- Enter 키로 전송
- 빈 메시지 방지
- 로딩 상태 처리
- 예시 질문 클릭
- 출처 표시
- 연속 메시지 처리
- 자동 스크롤

#### 네비게이션 (navigation.spec.ts)
- 홈 ↔ 채팅 페이지 이동
- 헤더 링크 네비게이션
- 푸터 링크 표시
- 브라우저 뒤로가기
- 404 페이지 처리
- 반응형 (모바일, 태블릿)

#### 접근성 (accessibility.spec.ts)
- 자동 접근성 스캔 (axe-core)
- 키보드 네비게이션
- ARIA 레이블
- 색상 대비 (WCAG AA)
- 스크린 리더 지원
- 폼 라벨
- 포커스 표시
- 200% 줌 지원

---

## 테스트 실행 순서 (CI/CD)

### 1. 백엔드 테스트
```bash
cd backend
pytest --cov=app --cov-report=term-missing
```

### 2. 프론트엔드 단위 테스트
```bash
cd frontend
npm test -- --coverage --watchAll=false
```

### 3. E2E 테스트 (선택)
```bash
cd frontend
npm run test:e2e
```

---

## 테스트 작성 가이드

### 백엔드 (pytest)

#### 단위 테스트 예시
```python
import pytest

@pytest.mark.unit
def test_example():
    # Arrange
    input_data = "테스트"
    
    # Act
    result = some_function(input_data)
    
    # Assert
    assert result is not None
    assert result == expected_value
```

#### 픽스처 사용
```python
def test_with_db(db_session):
    # db_session fixture 사용
    item = MyModel(name="테스트")
    db_session.add(item)
    db_session.commit()
    
    assert item.id is not None
```

### 프론트엔드 (Jest + React Testing Library)

#### 컴포넌트 테스트 예시
```typescript
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'

test('버튼 클릭 테스트', async () => {
  const user = userEvent.setup()
  const handleClick = jest.fn()
  
  render(<Button onClick={handleClick}>클릭</Button>)
  
  await user.click(screen.getByRole('button'))
  
  expect(handleClick).toHaveBeenCalled()
})
```

### E2E (Playwright)

#### 시나리오 테스트 예시
```typescript
import { test, expect } from '@playwright/test'

test('사용자 플로우', async ({ page }) => {
  await page.goto('/')
  
  await page.getByRole('button', { name: '시작' }).click()
  
  await expect(page).toHaveURL('/chat')
})
```

---

## 트러블슈팅

### 백엔드

**문제**: ImportError: cannot import name ...
- **해결**: `pip install -r requirements.txt` 재실행

**문제**: Database connection error
- **해결**: pytest는 SQLite 인메모리 DB 사용, PostgreSQL 불필요

**문제**: Tests fail with Claude API error
- **해결**: Mock 사용하므로 실제 API 키 불필요. Mock이 제대로 작동하는지 확인

### 프론트엔드

**문제**: Cannot find module '@testing-library/react'
- **해결**: `npm install` 재실행

**문제**: Playwright tests timeout
- **해결**: 서버가 실행 중인지 확인 (`npm run dev`)

**문제**: 접근성 테스트 실패
- **해결**: 컴포넌트에 적절한 ARIA 속성 추가

---

## 커버리지 목표

### 백엔드
- **전체**: 80% 이상
- **핵심 서비스** (AI, RAG): 90% 이상
- **API 엔드포인트**: 85% 이상

### 프론트엔드
- **전체**: 70% 이상
- **핵심 컴포넌트** (Chat): 85% 이상
- **Hooks**: 80% 이상

### E2E
- **핵심 사용자 플로우**: 100% 커버

---

## CI/CD 통합

### GitHub Actions 예시
```yaml
name: Tests

on: [push, pull_request]

jobs:
  backend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
      - name: Run tests
        run: |
          cd backend
          pytest --cov=app
  
  frontend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Node
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      - name: Install dependencies
        run: |
          cd frontend
          npm install
      - name: Run tests
        run: |
          cd frontend
          npm test -- --coverage --watchAll=false
```

---

## 테스트 베스트 프랙티스

### 일반
1. ✅ 테스트는 독립적이어야 함 (다른 테스트에 의존 X)
2. ✅ 테스트 이름은 명확하게 (무엇을 테스트하는지)
3. ✅ AAA 패턴 사용 (Arrange, Act, Assert)
4. ✅ 실제 사용 시나리오 테스트
5. ✅ 엣지 케이스 포함

### 백엔드
1. ✅ Mock 사용하여 외부 의존성 제거
2. ✅ 데이터베이스는 인메모리 사용
3. ✅ 비동기 함수는 pytest-asyncio 사용

### 프론트엔드
1. ✅ 구현이 아닌 사용자 행동 테스트
2. ✅ getByRole 등 시맨틱 쿼리 우선 사용
3. ✅ userEvent 사용 (fireEvent 대신)
4. ✅ 접근성 고려

---

**작성일**: 2026-01-22  
**버전**: 1.0

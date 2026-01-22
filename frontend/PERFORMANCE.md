# 프론트엔드 성능 최적화 가이드

## Next.js 최적화 설정

### 1. 이미지 최적화
- AVIF, WebP 포맷 자동 변환
- 반응형 이미지 크기 자동 조정
- 캐시 TTL 설정

### 2. 코드 스플리팅
- 자동 청크 분할
- React 라이브러리 별도 청크
- UI 컴포넌트 별도 청크
- 공통 모듈 추출

### 3. 압축 및 최적화
- GZIP 압축 활성화
- SWC 컴파일러 사용
- 프로덕션 소스맵 비활성화

### 4. 캐싱 전략
- 정적 파일: 1년 캐싱
- API 응답: 5분~1시간 (엔드포인트별)
- 이미지: 1분 캐싱

## 컴포넌트 레벨 최적화

### 동적 임포트 (Lazy Loading)
```typescript
import dynamic from 'next/dynamic';

// 무거운 컴포넌트는 동적 임포트
const HeavyComponent = dynamic(() => import('./HeavyComponent'), {
  loading: () => <div>로딩 중...</div>,
  ssr: false, // 클라이언트 사이드에서만 렌더링
});
```

### React.memo 사용
```typescript
import { memo } from 'react';

const ExpensiveComponent = memo(({ data }) => {
  // 렌더링 로직
});
```

### useMemo / useCallback 활용
```typescript
const memoizedValue = useMemo(() => computeExpensiveValue(a, b), [a, b]);
const memoizedCallback = useCallback(() => doSomething(a, b), [a, b]);
```

## 빌드 최적화

### 빌드 명령어
```bash
# 프로덕션 빌드 (최적화 적용)
npm run build

# 빌드 분석
npm run build && npm run analyze
```

### 환경 변수
프로덕션 환경에서는 `.env.production` 사용:
```
NEXT_PUBLIC_API_URL=https://api.example.com
NODE_ENV=production
```

## 성능 측정

### Lighthouse
1. Chrome DevTools > Lighthouse 탭
2. Performance, Accessibility 점수 확인

### Next.js 분석
```bash
npm install --save-dev @next/bundle-analyzer

# next.config.ts에 추가
const withBundleAnalyzer = require('@next/bundle-analyzer')({
  enabled: process.env.ANALYZE === 'true',
})
```

## 추가 최적화 팁

1. **폰트 최적화**: `next/font` 사용
2. **이미지 최적화**: `next/image` 사용
3. **링크 프리페칭**: `next/link` 자동 프리페칭 활용
4. **API 요청 최소화**: SWR 또는 React Query 사용
5. **CSS 최적화**: CSS Modules, Tailwind CSS 사용

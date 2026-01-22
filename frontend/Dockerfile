# 멀티 스테이지 빌드를 사용한 프로덕션 Dockerfile

# Stage 1: 의존성 설치
FROM node:20-alpine AS deps

WORKDIR /app

# 보안 업데이트
RUN apk add --no-cache libc6-compat

# package.json과 package-lock.json 복사
COPY package*.json ./

# 의존성 설치 (개발 의존성 포함 - 빌드에 필요)
RUN npm ci

# Stage 2: 빌드
FROM node:20-alpine AS builder

WORKDIR /app

# 의존성 복사
COPY --from=deps /app/node_modules ./node_modules
COPY . .

# 환경 변수 (빌드 시)
ARG NEXT_PUBLIC_API_URL
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL \
    NODE_ENV=production

# Next.js 빌드 (standalone 모드)
RUN npm run build

# Stage 3: 실행
FROM node:20-alpine AS runner

WORKDIR /app

ENV NODE_ENV=production \
    NODE_OPTIONS="--max-old-space-size=512"

# 보안 업데이트
RUN apk add --no-cache \
    curl \
    tini

# 사용자 추가 (보안)
RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 nextjs

# 필요한 파일만 복사
COPY --from=builder /app/public ./public

# next.config.ts에서 output: 'standalone' 설정이 필요
# standalone 빌드가 없는 경우를 위한 대안
COPY --from=builder --chown=nextjs:nodejs /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json

# 사용자 전환
USER nextjs

EXPOSE 3000

ENV PORT=3000 \
    HOSTNAME="0.0.0.0"

# Health check (curl 사용)
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:3000/ || exit 1

# Tini를 사용하여 신호 처리 개선
ENTRYPOINT ["/sbin/tini", "--"]

# Next.js 시작
CMD ["npm", "start"]

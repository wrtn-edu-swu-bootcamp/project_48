# 멀티 스테이지 빌드를 사용한 프로덕션 Dockerfile

# Stage 1: 빌드 스테이지
FROM python:3.11-slim as builder

WORKDIR /app

# 시스템 의존성 설치
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    postgresql-client \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Python 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --user -r requirements.txt

# Stage 2: 실행 스테이지
FROM python:3.11-slim

WORKDIR /app

# 비root 사용자 생성 (보안)
RUN groupadd -r appuser && useradd -r -g appuser appuser

# 시스템 의존성 (런타임만)
RUN apt-get update && apt-get install -y \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 빌드 스테이지에서 Python 패키지 복사
COPY --from=builder /root/.local /root/.local

# 애플리케이션 코드 복사
COPY --chown=appuser:appuser . .

# 로그 디렉토리 생성 및 권한 설정
RUN mkdir -p /app/logs && chown -R appuser:appuser /app/logs

# PATH에 로컬 bin 추가
ENV PATH=/root/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# 사용자 전환
USER appuser

# 포트 노출
EXPOSE 8000

# Health check (curl 사용)
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# 애플리케이션 실행 (Gunicorn + Uvicorn worker)
# 환경 변수로 workers 수 조정 가능 (기본값: 4)
CMD gunicorn app.main:app \
    --workers ${WORKERS:-4} \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:8000 \
    --timeout 120 \
    --graceful-timeout 30 \
    --keep-alive 5 \
    --max-requests ${MAX_REQUESTS:-1000} \
    --max-requests-jitter ${MAX_REQUESTS_JITTER:-100} \
    --access-logfile /app/logs/access.log \
    --error-logfile /app/logs/error.log \
    --log-level ${LOG_LEVEL:-info}

# 🎯 시스템 실행 전 체크리스트

## ✅ 준비 확인

### 1. 환경 변수 설정
- [ ] `.env` 파일 생성 완료
- [ ] `ANTHROPIC_API_KEY` 설정 완료
- [ ] 기타 환경 변수 확인

### 2. Docker 환경
- [ ] Docker Desktop 실행 중
- [ ] Docker Compose 설치 확인: `docker-compose --version`

### 3. 포트 확인 (충돌 방지)
- [ ] 포트 5432 (PostgreSQL) 사용 가능
- [ ] 포트 6379 (Redis) 사용 가능
- [ ] 포트 8000 (Backend) 사용 가능
- [ ] 포트 3000 (Frontend) 사용 가능

---

## 🚀 실행 명령어 (순서대로)

```bash
# 1. 환경 변수 파일 복사 및 편집
cp env.development.example .env
# .env 파일에서 ANTHROPIC_API_KEY 수정

# 2. Docker Compose로 전체 시스템 시작
docker-compose up -d

# 3. 로그 확인 (서비스 시작 확인)
docker-compose logs -f

# 4. 초기 데이터 입력 (새 터미널에서)
docker-compose exec backend bash
cd ..
python scripts/seed_data.py
python scripts/generate_embeddings.py
exit

# 5. 헬스 체크
curl http://localhost:8000/health

# 6. 브라우저에서 접속
# http://localhost:3000
```

---

## 🧪 테스트 질문 예시

시스템이 정상 실행되면 다음 질문들을 테스트해보세요:

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

## 📊 확인 사항

### 1. 서비스 상태
```bash
docker-compose ps
```

모든 서비스가 `Up (healthy)` 상태여야 합니다.

### 2. 백엔드 API
```bash
# 헬스 체크
curl http://localhost:8000/health

# API 문서
# 브라우저: http://localhost:8000/docs
```

### 3. 프론트엔드
```bash
# 브라우저: http://localhost:3000
```

### 4. 데이터베이스
```bash
# PostgreSQL 접속
docker-compose exec postgres psql -U postgres -d swu_chatbot

# 데이터 확인
\dt
SELECT COUNT(*) FROM academic_schedules;
SELECT COUNT(*) FROM notices;
SELECT COUNT(*) FROM support_programs;
SELECT COUNT(*) FROM academic_glossary;
\q
```

### 5. Redis 캐시
```bash
# Redis 접속
docker-compose exec redis redis-cli

# 키 확인
KEYS *
INFO
exit
```

---

## ⚠️ 주의사항

1. **첫 실행 시 시간 소요**
   - Docker 이미지 다운로드 및 빌드: 5-10분
   - 데이터베이스 초기화: 1-2분
   - 임베딩 생성: 2-3분

2. **API 키 필수**
   - ANTHROPIC_API_KEY가 없으면 AI 응답 불가
   - 환경 변수 설정 후 서비스 재시작 필요

3. **리소스 요구사항**
   - RAM: 최소 4GB, 권장 8GB
   - Disk: 최소 5GB 여유 공간

4. **Windows 사용자**
   - Docker Desktop에서 WSL2 사용 권장
   - 파일 공유 설정 필요할 수 있음

---

## 🐛 문제 발생 시

### 서비스가 시작되지 않음
```bash
# 로그 확인
docker-compose logs backend
docker-compose logs postgres

# 재시작
docker-compose restart

# 완전 재시작
docker-compose down
docker-compose up -d
```

### 데이터베이스 연결 오류
```bash
# PostgreSQL 상태 확인
docker-compose exec postgres pg_isready -U postgres

# 마이그레이션 재실행
docker-compose exec backend alembic upgrade head
```

### 캐시 문제
```bash
# Redis 캐시 초기화
docker-compose exec redis redis-cli FLUSHALL

# 서비스 재시작
docker-compose restart backend
```

---

## 📝 실행 로그 예시

정상 실행 시 다음과 같은 로그를 볼 수 있습니다:

```
✓ PostgreSQL is ready
✓ Redis is ready
✓ Running migrations...
✓ Starting server...
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

---

**준비가 되었다면 `docker-compose up -d` 명령으로 시작하세요! 🎉**

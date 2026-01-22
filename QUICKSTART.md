# 빠른 시작 가이드 🚀

이 가이드를 따라하면 5분 안에 AI 신입생 도우미를 실행할 수 있습니다.

---

## 📋 사전 준비

설치가 필요한 것들:
- [ ] Python 3.10 이상
- [ ] Node.js 18 이상
- [ ] Anthropic API 키 (https://console.anthropic.com/)

---

## ⚡ 초고속 실행 (SQLite 개발 모드)

### 1단계: 백엔드 설정 (2분)

```bash
# 백엔드 폴더로 이동
cd backend

# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 패키지 설치
pip install -r requirements.txt

# 환경 변수 설정
echo 'DATABASE_URL=sqlite:///./ai_freshman_helper.db
ANTHROPIC_API_KEY=sk-ant-여기에-API키-입력
EMBEDDING_MODEL=sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
DEBUG=True' > .env

# 데이터베이스 초기화
cd ..
python scripts/init_db.py
python scripts/seed_data.py

# 백엔드 실행
cd backend
uvicorn app.main:app --reload
```

✅ 백엔드가 http://localhost:8000에서 실행됩니다!

### 2단계: 프론트엔드 설정 (2분)

**새 터미널을 열고:**

```bash
# 프론트엔드 폴더로 이동
cd frontend

# 패키지 설치
npm install

# 환경 변수 설정
echo 'NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1' > .env.local

# 프론트엔드 실행
npm run dev
```

✅ 프론트엔드가 http://localhost:3000에서 실행됩니다!

### 3단계: 접속하기

브라우저에서 http://localhost:3000을 열면 끝! 🎉

---

## 🔍 문제 해결

### 백엔드가 실행되지 않을 때

**문제 1**: `ModuleNotFoundError`
```bash
# 해결: 가상환경을 활성화했는지 확인
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**문제 2**: `ANTHROPIC_API_KEY not found`
```bash
# 해결: .env 파일에 API 키가 있는지 확인
cat backend/.env  # Windows: type backend\.env

# API 키가 없다면 다시 생성
cd backend
echo 'ANTHROPIC_API_KEY=sk-ant-여기에-진짜-API키-입력' >> .env
```

**문제 3**: 데이터베이스 오류
```bash
# 해결: 데이터베이스를 다시 초기화
cd backend
rm ai_freshman_helper.db  # 기존 DB 삭제
cd ..
python scripts/init_db.py
python scripts/seed_data.py
```

### 프론트엔드가 실행되지 않을 때

**문제 1**: `Cannot find module`
```bash
# 해결: node_modules를 다시 설치
cd frontend
rm -rf node_modules package-lock.json  # Windows: rmdir /s node_modules
npm install
```

**문제 2**: `Cannot connect to backend`
```bash
# 해결: 백엔드가 실행 중인지 확인
curl http://localhost:8000/health

# 응답이 없다면 백엔드를 다시 시작
cd backend
uvicorn app.main:app --reload
```

---

## 🧪 동작 확인

### 1. 백엔드 API 테스트

브라우저에서 http://localhost:8000/docs를 열고:
- "GET /health" 엔드포인트를 클릭
- "Try it out" 버튼 클릭
- "Execute" 버튼 클릭
- 응답이 `{"status": "healthy"}`인지 확인

### 2. 프론트엔드 테스트

브라우저에서 http://localhost:3000을 열고:
- "지금 질문하기" 버튼 클릭
- 채팅창에 "수강신청은 언제 하나요?" 입력
- AI 답변이 나오는지 확인

---

## 🎯 다음 단계

### 임베딩 생성 (선택사항, 검색 품질 향상)

```bash
# 백엔드가 실행 중이면 먼저 중지 (Ctrl+C)
cd ..
python scripts/generate_embeddings.py

# 완료되면 백엔드 다시 실행
cd backend
uvicorn app.main:app --reload
```

이 작업은 5-10분 정도 소요됩니다. 임베딩을 생성하면 벡터 검색이 활성화되어 더 정확한 답변을 받을 수 있습니다.

### 데이터 추가

초기 데이터는 `scripts/data/` 폴더에 있습니다:
- `academic_schedules.json` - 학사 일정
- `notices.json` - 공지사항
- `support_programs.json` - 지원 프로그램
- `glossary.json` - 학사 용어

JSON 파일을 수정한 후:
```bash
python scripts/seed_data.py
python scripts/generate_embeddings.py  # 임베딩 재생성
```

---

## 📱 모바일에서 테스트하기

같은 Wi-Fi 네트워크에 연결된 모바일 기기에서:

1. 컴퓨터의 IP 주소 확인:
```bash
# Windows
ipconfig

# Mac/Linux
ifconfig
```

2. 모바일 브라우저에서 접속:
```
http://[컴퓨터-IP]:3000
```

예: `http://192.168.0.100:3000`

---

## 🎓 예시 질문

다음 질문들을 시도해보세요:

1. **학사 일정**
   - "수강신청은 언제 하나요?"
   - "1학기 등록금 납부 기간이 언제예요?"
   - "중간고사는 언제인가요?"

2. **지원 프로그램**
   - "장학금 신청 방법이 궁금해요"
   - "비교과 프로그램에는 뭐가 있나요?"
   - "멘토링 프로그램 신청하고 싶어요"

3. **학사 용어**
   - "복수전공이 뭔가요?"
   - "학점제가 어떻게 되나요?"
   - "수강중도포기가 뭔가요?"

4. **공지사항**
   - "최근 공지사항 알려주세요"
   - "장학금 관련 공지 있나요?"

---

## 💡 팁

### 개발 팁
- 백엔드 코드 수정 시 자동으로 재시작됩니다 (`--reload` 옵션)
- 프론트엔드 코드 수정 시 Hot Reload가 됩니다
- API 문서는 http://localhost:8000/docs에서 확인

### 성능 팁
- 첫 실행 시 임베딩 모델 다운로드로 시간이 걸릴 수 있습니다
- SQLite 대신 PostgreSQL을 사용하면 더 빠른 벡터 검색이 가능합니다
- 프로덕션에서는 `DEBUG=False`로 설정하세요

---

## 📞 도움이 필요하신가요?

- 📖 상세 가이드: `DEVELOPMENT_GUIDE.md` 참조
- 🏗️ 아키텍처: `docs/Architecture.md` 참조
- 🐛 버그 리포트: GitHub Issues 활용

---

**Happy Coding! 🚀**

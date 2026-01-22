"""
간단한 데모 서버 - 지금까지 개발한 API 구조 확인용
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

app = FastAPI(
    title="AI 신입생 도우미 API - 데모",
    version="1.0.0",
    description="서울여자대학교 신입생을 위한 AI 챗봇 (데모 버전)"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 스키마 정의
class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

class Source(BaseModel):
    type: str
    title: str
    content: str

class ChatResponse(BaseModel):
    answer: str
    sources: List[Source] = []
    timestamp: str

class Schedule(BaseModel):
    id: int
    title: str
    category: str
    start_date: str
    end_date: str
    description: str

class Notice(BaseModel):
    id: int
    title: str
    category: str
    importance: str
    posted_date: str
    content: str

class Program(BaseModel):
    id: int
    title: str
    category: str
    department: str
    application_start: Optional[str]
    application_end: Optional[str]
    description: str

# 데모 데이터
DEMO_RESPONSE = {
    "answer": """안녕하세요! AI 신입생 도우미입니다. 🎓

저는 서울여자대학교 신입생 여러분을 위해 다음과 같은 정보를 제공합니다:

📅 **학사 일정**
• 수강신청 일정
• 시험 기간 (중간고사, 기말고사)
• 등록금 납부 기간
• 방학 일정

💰 **지원 프로그램**
• 장학금 신청 방법
• 비교과 프로그램
• 취업 지원 프로그램
• 멘토링 프로그램

📢 **공지사항**
• 학사 공지
• 장학 공지
• 취업 공지

📚 **학사 용어**
• 복수전공, 부전공
• 학점제, GPA
• 휴학, 복학 안내

**실제 질문 예시:**
"수강신청은 언제 하나요?"
"장학금 신청 방법이 궁금해요"
"복수전공이 뭔가요?"

현재는 데모 모드로 실행 중입니다. 
실제 AI 기능을 사용하려면 PostgreSQL과 Anthropic API 키가 필요합니다.""",
    "sources": [
        {"type": "시스템", "title": "AI 신입생 도우미 데모", "content": "개발 완료: 90%"}
    ]
}

DEMO_SCHEDULES = [
    {
        "id": 1,
        "title": "2024학년도 1학기 수강신청 (신입생)",
        "category": "수강신청",
        "start_date": "2024-02-19",
        "end_date": "2024-02-21",
        "description": "2024학년도 1학기 신입생 수강신청 기간"
    },
    {
        "id": 2,
        "title": "2024학년도 1학기 중간고사",
        "category": "시험",
        "start_date": "2024-04-15",
        "end_date": "2024-04-19",
        "description": "1학기 중간고사 기간"
    }
]

DEMO_NOTICES = [
    {
        "id": 1,
        "title": "2024학년도 1학기 국가장학금 신청 안내",
        "category": "장학",
        "importance": "high",
        "posted_date": "2024-01-15",
        "content": "한국장학재단 국가장학금 신청 기간 및 방법 안내"
    }
]

DEMO_PROGRAMS = [
    {
        "id": 1,
        "title": "성적우수장학금",
        "category": "장학",
        "department": "학생지원팀",
        "application_start": "2024-03-01",
        "application_end": "2024-03-31",
        "description": "직전 학기 성적우수자 대상 장학금"
    }
]

@app.get("/")
def root():
    """루트 엔드포인트"""
    return {
        "message": "AI 신입생 도우미 API - 데모 모드",
        "version": "1.0.0",
        "status": "running",
        "features": {
            "implemented": [
                "RAG 파이프라인",
                "벡터 검색",
                "Claude AI 연동",
                "질문 분류",
                "답변 검증",
                "캐싱 시스템",
                "성능 모니터링"
            ],
            "completion": "90%",
            "remaining": ["배포 설정", "운영 모니터링"]
        }
    }

@app.get("/health")
def health_check():
    """헬스 체크"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "database": "demo-mode",
        "ai_service": "demo-mode"
    }

@app.post("/api/v1/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    """채팅 API - 데모 응답"""
    return ChatResponse(
        answer=DEMO_RESPONSE["answer"],
        sources=[Source(**s) for s in DEMO_RESPONSE["sources"]],
        timestamp=datetime.now().isoformat()
    )

@app.get("/api/v1/schedules", response_model=List[Schedule])
def get_schedules(category: Optional[str] = None):
    """학사일정 API"""
    schedules = DEMO_SCHEDULES
    if category:
        schedules = [s for s in schedules if s["category"] == category]
    return schedules

@app.get("/api/v1/schedules/{schedule_id}", response_model=Schedule)
def get_schedule(schedule_id: int):
    """학사일정 상세 API"""
    schedule = next((s for s in DEMO_SCHEDULES if s["id"] == schedule_id), None)
    if not schedule:
        raise HTTPException(status_code=404, detail="일정을 찾을 수 없습니다")
    return schedule

@app.get("/api/v1/notices", response_model=List[Notice])
def get_notices(category: Optional[str] = None):
    """공지사항 API"""
    notices = DEMO_NOTICES
    if category:
        notices = [n for n in notices if n["category"] == category]
    return notices

@app.get("/api/v1/programs", response_model=List[Program])
def get_programs(category: Optional[str] = None):
    """지원프로그램 API"""
    programs = DEMO_PROGRAMS
    if category:
        programs = [p for p in programs if p["category"] == category]
    return programs

@app.get("/api/v1/stats")
def get_stats():
    """개발 통계"""
    return {
        "completion_rate": "90%",
        "components": {
            "backend": {
                "api_endpoints": 4,
                "ai_services": 7,
                "models": 6,
                "tests": 10,
                "status": "완료"
            },
            "frontend": {
                "components": 9,
                "pages": 2,
                "hooks": 1,
                "status": "완료"
            },
            "database": {
                "tables": 6,
                "initial_data": 52,
                "migrations": 2,
                "status": "완료"
            },
            "optimization": {
                "caching": "Redis",
                "rate_limiting": "100/min",
                "compression": "GZIP",
                "monitoring": "구현완료",
                "status": "완료"
            }
        },
        "next_phase": "배포 준비 (Docker, CI/CD)"
    }

if __name__ == "__main__":
    import uvicorn
    import sys
    
    # Windows 인코딩 설정
    if sys.platform == 'win32':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except:
            pass
    
    print("=" * 60)
    print("AI Freshman Helper - Demo Server")
    print("=" * 60)
    print("Server: http://localhost:8000")
    print("API Docs: http://localhost:8000/docs")
    print("Stats: http://localhost:8000/api/v1/stats")
    print("=" * 60)
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")

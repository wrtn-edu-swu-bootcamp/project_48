"""
챗봇 관련 Pydantic 스키마
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime


class ChatRequest(BaseModel):
    """챗봇 질문 요청 스키마"""
    message: str = Field(..., description="질문 내용", min_length=1, max_length=1000)
    session_id: Optional[str] = Field(None, description="세션 ID")
    
    # 내부에서 question으로도 접근 가능하도록
    @property
    def question(self) -> str:
        return self.message


class ChatResponse(BaseModel):
    """챗봇 답변 응답 스키마"""
    answer: str = Field(..., description="답변 내용")
    sources: Optional[List[Dict[str, str]]] = Field(default_factory=list, description="출처 목록")
    related_questions: Optional[List[str]] = Field(None, description="관련 질문")
    category: Optional[str] = Field(None, description="질문 분류")


class FeedbackRequest(BaseModel):
    """피드백 요청 스키마"""
    message_id: int = Field(..., description="메시지 ID")
    feedback: str = Field(..., description="피드백 타입 (positive/negative)")
    comment: Optional[str] = Field(None, description="피드백 코멘트")

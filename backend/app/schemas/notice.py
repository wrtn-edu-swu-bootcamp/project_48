"""
공지사항 Pydantic 스키마
"""
from pydantic import BaseModel
from datetime import date
from typing import Optional
from app.models.notice import NoticeType, ImportanceLevel


class NoticeResponse(BaseModel):
    """공지사항 응답 스키마"""
    id: int
    title: str
    content: str
    notice_type: NoticeType
    importance: ImportanceLevel
    department: Optional[str] = None
    created_at: date
    updated_at: Optional[date] = None
    is_active: int

    class Config:
        from_attributes = True
"""
지원 프로그램 Pydantic 스키마
"""
from pydantic import BaseModel
from datetime import date
from typing import Optional
from app.models.support_program import ProgramType


class SupportProgramResponse(BaseModel):
    """지원 프로그램 응답 스키마"""
    id: int
    name: str
    program_type: ProgramType
    application_start: Optional[date] = None
    application_end: Optional[date] = None
    target: Optional[str] = None
    application_method: Optional[str] = None
    requirements: Optional[str] = None
    documents: Optional[str] = None
    benefits: Optional[str] = None
    description: Optional[str] = None
    created_at: date
    updated_at: Optional[date] = None
    is_active: int

    class Config:
        from_attributes = True
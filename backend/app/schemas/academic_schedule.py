"""
학사 일정 Pydantic 스키마
"""
from pydantic import BaseModel
from datetime import date
from typing import Optional
from app.models.academic_schedule import SemesterType, ScheduleType


class AcademicScheduleResponse(BaseModel):
    """학사 일정 응답 스키마"""
    id: int
    name: str
    start_date: date
    end_date: Optional[date] = None
    semester: SemesterType
    schedule_type: ScheduleType
    description: Optional[str] = None
    importance: int
    created_at: date
    updated_at: Optional[date] = None

    class Config:
        from_attributes = True
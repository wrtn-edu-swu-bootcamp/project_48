"""
학사 일정 모델
"""
from sqlalchemy import Column, Integer, String, Date, Text, Enum
from sqlalchemy.types import Enum as SQLEnum
from pgvector.sqlalchemy import Vector
import enum
from app.core.database import Base


class SemesterType(str, enum.Enum):
    """학기 타입"""
    FIRST = "1학기"
    SECOND = "2학기"
    SUMMER = "여름 계절학기"
    WINTER = "겨울 계절학기"


class ScheduleType(str, enum.Enum):
    """일정 유형"""
    COURSE_REGISTRATION = "수강신청"
    TUITION_PAYMENT = "등록금 납부"
    VACATION = "휴학/복학"
    EXAM = "시험"
    GRADE = "성적 입력"
    OTHER = "기타"


class AcademicSchedule(Base):
    """학사 일정 모델"""
    __tablename__ = "academic_schedules"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, comment="일정명")
    start_date = Column(Date, nullable=False, comment="시작일")
    end_date = Column(Date, nullable=True, comment="종료일")
    semester = Column(SQLEnum(SemesterType), nullable=False, comment="학기")
    schedule_type = Column(SQLEnum(ScheduleType), nullable=False, comment="일정 유형")
    description = Column(Text, nullable=True, comment="설명")
    importance = Column(Integer, default=0, comment="중요도 (0-10)")
    embedding = Column(Vector(384), nullable=True, comment="벡터 임베딩 (384차원)")
    created_at = Column(Date, nullable=False, comment="생성일")
    updated_at = Column(Date, nullable=True, comment="수정일")

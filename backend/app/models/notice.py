"""
공지사항 모델
"""
from sqlalchemy import Column, Integer, String, Text, Date, Enum
from sqlalchemy.types import Enum as SQLEnum
from pgvector.sqlalchemy import Vector
import enum
from app.core.database import Base


class NoticeType(str, enum.Enum):
    """공지 유형"""
    ACADEMIC = "학사"
    TUITION = "등록금"
    SCHOLARSHIP = "장학금"
    PROGRAM = "비교과 프로그램"
    OTHER = "기타"


class ImportanceLevel(str, enum.Enum):
    """중요도"""
    HIGH = "높음"
    MEDIUM = "보통"
    LOW = "낮음"


class Notice(Base):
    """공지사항 모델"""
    __tablename__ = "notices"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False, comment="제목")
    content = Column(Text, nullable=False, comment="내용")
    notice_type = Column(SQLEnum(NoticeType), nullable=False, comment="공지 유형")
    importance = Column(SQLEnum(ImportanceLevel), default=ImportanceLevel.MEDIUM, comment="중요도")
    department = Column(String(100), nullable=True, comment="부서 또는 학과")
    embedding = Column(Vector(384), nullable=True, comment="벡터 임베딩 (384차원)")
    created_at = Column(Date, nullable=False, comment="작성일")
    updated_at = Column(Date, nullable=True, comment="수정일")
    is_active = Column(Integer, default=1, comment="활성화 여부 (1: 활성, 0: 비활성)")

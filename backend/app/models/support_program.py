"""
지원 프로그램 모델
"""
from sqlalchemy import Column, Integer, String, Text, Date, Enum
from sqlalchemy.types import Enum as SQLEnum
from pgvector.sqlalchemy import Vector
import enum
from app.core.database import Base


class ProgramType(str, enum.Enum):
    """프로그램 유형"""
    SCHOLARSHIP = "장학금"
    EXTRACURRICULAR = "비교과 프로그램"
    MENTORING = "멘토링"
    EMPLOYMENT = "취업 지원"
    OTHER = "기타"


class SupportProgram(Base):
    """지원 프로그램 모델"""
    __tablename__ = "support_programs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, comment="프로그램명")
    program_type = Column(SQLEnum(ProgramType), nullable=False, comment="프로그램 유형")
    application_start = Column(Date, nullable=True, comment="신청 시작일")
    application_end = Column(Date, nullable=True, comment="신청 종료일")
    target = Column(Text, nullable=True, comment="대상")
    application_method = Column(Text, nullable=True, comment="신청 방법")
    requirements = Column(Text, nullable=True, comment="자격 요건")
    documents = Column(Text, nullable=True, comment="필요 서류")
    benefits = Column(Text, nullable=True, comment="혜택 및 지원 내용")
    description = Column(Text, nullable=True, comment="설명")
    embedding = Column(Vector(384), nullable=True, comment="벡터 임베딩 (384차원)")
    created_at = Column(Date, nullable=False, comment="생성일")
    updated_at = Column(Date, nullable=True, comment="수정일")
    is_active = Column(Integer, default=1, comment="활성화 여부 (1: 활성, 0: 비활성)")

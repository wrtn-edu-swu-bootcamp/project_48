"""
학사 용어 모델
"""
from sqlalchemy import Column, Integer, String, Text, Date
from app.core.database import Base


class AcademicTerm(Base):
    """학사 용어 모델"""
    __tablename__ = "academic_terms"

    id = Column(Integer, primary_key=True, index=True)
    term = Column(String(100), nullable=False, unique=True, comment="용어")
    definition = Column(Text, nullable=False, comment="정의")
    simple_explanation = Column(Text, nullable=True, comment="쉬운 설명")
    example = Column(Text, nullable=True, comment="예시")
    related_terms = Column(String(500), nullable=True, comment="관련 용어 (쉼표로 구분)")
    created_at = Column(Date, nullable=False, comment="생성일")
    updated_at = Column(Date, nullable=True, comment="수정일")

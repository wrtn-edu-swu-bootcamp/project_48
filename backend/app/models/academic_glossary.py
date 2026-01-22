"""
학사 용어 사전 모델
"""
from sqlalchemy import Column, Integer, String, Text, Date
from pgvector.sqlalchemy import Vector
from app.core.database import Base


class AcademicGlossary(Base):
    """학사 용어 사전 모델"""
    __tablename__ = "academic_glossary"

    id = Column(Integer, primary_key=True, index=True)
    term_ko = Column(String(200), nullable=False, comment="한국어 용어")
    term_en = Column(String(200), nullable=True, comment="영문 용어")
    definition = Column(Text, nullable=False, comment="정의 및 설명")
    examples = Column(Text, nullable=True, comment="예시")
    category = Column(String(100), nullable=True, comment="카테고리")
    embedding = Column(Vector(384), nullable=True, comment="벡터 임베딩 (384차원)")
    created_at = Column(Date, nullable=False, comment="생성일")
    updated_at = Column(Date, nullable=True, comment="수정일")

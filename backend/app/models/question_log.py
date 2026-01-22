"""
질문 로그 모델
"""
from sqlalchemy import Column, Integer, String, Text, Date, DateTime, Enum
from sqlalchemy.types import Enum as SQLEnum
import enum
from app.core.database import Base


class QuestionCategory(str, enum.Enum):
    """질문 분류"""
    ACADEMIC_SCHEDULE = "학사 일정"
    NOTICE = "공지사항"
    SUPPORT_PROGRAM = "지원 프로그램"
    ACADEMIC_INFO = "신입생 기본 정보"
    OTHER = "기타"


class QuestionStatus(str, enum.Enum):
    """질문 상태"""
    PENDING = "대기"
    PROCESSING = "처리 중"
    COMPLETED = "완료"
    FAILED = "실패"


class FeedbackType(str, enum.Enum):
    """피드백 타입"""
    POSITIVE = "positive"
    NEGATIVE = "negative"


class QuestionLog(Base):
    """질문 로그 모델"""
    __tablename__ = "question_logs"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text, nullable=False, comment="질문 내용")
    answer = Column(Text, nullable=True, comment="답변 내용")
    category = Column(SQLEnum(QuestionCategory), nullable=True, comment="질문 분류")
    status = Column(SQLEnum(QuestionStatus), default=QuestionStatus.PENDING, comment="상태")
    source = Column(String(500), nullable=True, comment="출처")
    feedback = Column(SQLEnum(FeedbackType), nullable=True, comment="피드백")
    feedback_comment = Column(Text, nullable=True, comment="피드백 코멘트")
    created_at = Column(DateTime, nullable=False, comment="생성일시")
    updated_at = Column(DateTime, nullable=True, comment="수정일시")

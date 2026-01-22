"""
폴백 메커니즘 - AI 실패 시 안전한 응답 제공
"""
from typing import Dict, Any
from app.models.question_log import QuestionCategory
import logging

logger = logging.getLogger(__name__)


class FallbackHandler:
    """폴백 핸들러 클래스"""
    
    def __init__(self):
        """폴백 응답 템플릿 초기화"""
        self.fallback_messages = {
            QuestionCategory.ACADEMIC_SCHEDULE: """죄송해요. 학사 일정 정보를 찾을 수 없어요.

**확인 방법:**
- 학사지원팀에 문의: 02-970-XXXX
- 학사시스템에서 학사일정 확인
- 학교 홈페이지 > 학사안내 > 학사일정

다른 궁금하신 점이 있으신가요?""",
            
            QuestionCategory.NOTICE: """죄송해요. 해당 공지사항을 찾을 수 없어요.

**확인 방법:**
- 학교 홈페이지 공지사항 확인
- 해당 부서에 직접 문의
- 학생성장지원시스템 확인

다른 궁금하신 점이 있으신가요?""",
            
            QuestionCategory.SUPPORT_PROGRAM: """죄송해요. 해당 지원 프로그램 정보를 찾을 수 없어요.

**확인 방법:**
- 학생지원팀에 문의: 02-970-XXXX
- 학생성장지원시스템 확인
- 대학일자리플러스사업단 문의

다른 궁금하신 점이 있으신가요?""",
            
            QuestionCategory.ACADEMIC_INFO: """죄송해요. 해당 학사 용어 정보를 찾을 수 없어요.

**확인 방법:**
- 학사지원팀에 문의
- 학생 편람 확인
- 학교 홈페이지 참고

다른 궁금하신 점이 있으신가요?""",
        }
        
        self.general_fallback = """죄송해요. 현재 해당 질문에 대한 정보를 찾을 수 없어요.

**추천 방법:**
- 질문을 다르게 표현해보세요
- 학교 행정실에 직접 문의해보세요 (02-970-XXXX)
- 아래 '상담원 연결' 버튼을 클릭해주세요

다른 궁금하신 점이 있으신가요?"""
    
    def get_fallback_response(
        self,
        question: str,
        category: QuestionCategory = None,
    ) -> Dict[str, Any]:
        """
        카테고리에 맞는 폴백 응답 반환
        
        Args:
            question: 사용자 질문
            category: 질문 카테고리
            
        Returns:
            폴백 응답
        """
        if category and category in self.fallback_messages:
            message = self.fallback_messages[category]
        else:
            message = self.general_fallback
        
        logger.info(f"폴백 응답 반환: {category}")
        
        return {
            "answer": message,
            "sources": [],
            "category": category.value if category else "unknown",
            "search_results_count": 0,
            "success": True,
            "is_fallback": True
        }
    
    def get_error_response(
        self,
        error_message: str = None,
    ) -> Dict[str, Any]:
        """
        에러 응답 반환
        
        Args:
            error_message: 에러 메시지 (선택)
            
        Returns:
            에러 응답
        """
        logger.error(f"에러 응답 반환: {error_message}")
        
        return {
            "answer": """죄송해요. 일시적인 오류가 발생했어요.

**해결 방법:**
- 잠시 후 다시 시도해주세요
- 문제가 계속되면 '상담원 연결'을 클릭해주세요
- 또는 학교 행정실에 직접 문의해주세요

불편을 드려 죄송합니다.""",
            "sources": [],
            "category": "error",
            "search_results_count": 0,
            "success": False,
            "error": error_message
        }


# 싱글톤 인스턴스
_fallback_handler = None


def get_fallback_handler() -> FallbackHandler:
    """폴백 핸들러 인스턴스 반환 (싱글톤)"""
    global _fallback_handler
    if _fallback_handler is None:
        _fallback_handler = FallbackHandler()
    return _fallback_handler

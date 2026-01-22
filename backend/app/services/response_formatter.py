"""
응답 구조화 서비스
"""
from app.schemas.chat import ChatResponse
from app.models.question_log import QuestionCategory
from typing import List, Dict, Any


class ResponseFormatter:
    """응답 구조화기"""
    
    def format_response(
        self,
        question: str,
        category: QuestionCategory,
        search_results: List[Dict[str, Any]],
    ) -> ChatResponse:
        """
        검색 결과를 기반으로 구조화된 응답을 생성합니다.
        
        기획안.md 섹션 4.3 응답 구조 규칙 참조:
        - 한 줄 요약
        - 자세한 설명
        - 다음 행동 가이드
        - 출처 표기
        """
        if not search_results:
            return ChatResponse(
                answer="해당 내용은 현재 제공된 정보에서 확인되지 않아요. 학교 행정실이나 학과 사무실에 직접 문의해보시는 것을 권장드려요.",
                source="AI 신입생 도우미",
            )
        
        # 첫 번째 검색 결과를 기본으로 사용
        result = search_results[0]
        
        # 카테고리별 응답 형식
        if category == QuestionCategory.ACADEMIC_SCHEDULE:
            answer = self._format_schedule_response(result)
        elif category == QuestionCategory.NOTICE:
            answer = self._format_notice_response(result)
        elif category == QuestionCategory.SUPPORT_PROGRAM:
            answer = self._format_program_response(result)
        elif category == QuestionCategory.ACADEMIC_INFO:
            answer = self._format_term_response(result)
        else:
            answer = self._format_generic_response(result)
        
        return ChatResponse(
            answer=answer,
            source=result.get("source", "AI 신입생 도우미"),
            category=category.value,
        )
    
    def _format_schedule_response(self, result: Dict[str, Any]) -> str:
        """학사 일정 응답 형식"""
        summary = f"{result.get('name', '학사 일정')}에 대한 안내입니다."
        details = result.get("description", "")
        action = "자세한 내용은 학교 홈페이지를 확인해주세요."
        
        return f"{summary}\n\n{details}\n\n{action}"
    
    def _format_notice_response(self, result: Dict[str, Any]) -> str:
        """공지사항 응답 형식"""
        summary = f"{result.get('title', '공지사항')}에 대한 안내입니다."
        details = result.get("content", "")[:500]  # 처음 500자만
        action = "전체 내용은 학교 홈페이지에서 확인해주세요."
        
        return f"{summary}\n\n{details}\n\n{action}"
    
    def _format_program_response(self, result: Dict[str, Any]) -> str:
        """지원 프로그램 응답 형식"""
        summary = f"{result.get('name', '지원 프로그램')}에 대한 안내입니다."
        details = result.get("description", "")
        action = f"신청 방법: {result.get('application_method', '학교 홈페이지에서 확인해주세요.')}"
        
        return f"{summary}\n\n{details}\n\n{action}"
    
    def _format_term_response(self, result: Dict[str, Any]) -> str:
        """학사 용어 응답 형식"""
        term = result.get("term", "")
        simple_explanation = result.get("simple_explanation", result.get("definition", ""))
        example = result.get("example", "")
        
        answer = f"{term}은(는) {simple_explanation}"
        if example:
            answer += f"\n\n예시: {example}"
        
        return answer
    
    def _format_generic_response(self, result: Dict[str, Any]) -> str:
        """일반 응답 형식"""
        return result.get("description", result.get("content", "정보를 찾을 수 없습니다."))

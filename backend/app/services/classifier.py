"""
질문 분류 서비스
"""
from app.models.question_log import QuestionCategory
from typing import Dict, List


class QuestionClassifier:
    """질문 분류기"""
    
    # 키워드 기반 분류 (초기 버전, 향후 AI 기반으로 확장 가능)
    KEYWORDS: Dict[QuestionCategory, List[str]] = {
        QuestionCategory.ACADEMIC_SCHEDULE: [
            "수강신청", "등록금", "휴학", "복학", "시험", "성적", "일정", "기간"
        ],
        QuestionCategory.NOTICE: [
            "공지", "안내", "발표", "알림"
        ],
        QuestionCategory.SUPPORT_PROGRAM: [
            "장학금", "비교과", "멘토링", "취업", "프로그램", "지원"
        ],
        QuestionCategory.ACADEMIC_INFO: [
            "학점", "전공", "복수전공", "부전공", "용어", "제도", "규정"
        ],
    }
    
    def classify(self, question: str) -> QuestionCategory:
        """
        질문을 분류합니다.
        
        Args:
            question: 사용자 질문
            
        Returns:
            QuestionCategory: 분류된 카테고리
        """
        question_lower = question.lower()
        
        # 각 카테고리별 키워드 매칭 점수 계산
        scores: Dict[QuestionCategory, int] = {
            category: 0 for category in QuestionCategory
        }
        
        for category, keywords in self.KEYWORDS.items():
            for keyword in keywords:
                if keyword in question_lower:
                    scores[category] += 1
        
        # 가장 높은 점수의 카테고리 반환
        if max(scores.values()) > 0:
            return max(scores.items(), key=lambda x: x[1])[0]
        
        # 매칭되는 키워드가 없으면 기타로 분류
        return QuestionCategory.OTHER

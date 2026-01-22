"""
답변 검증기
"""
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


class AnswerValidator:
    """답변 검증기 클래스"""
    
    def validate_answer(self, answer: str, sources: list) -> Dict[str, Any]:
        """
        답변이 적절한지 검증
        
        Args:
            answer: 생성된 답변
            sources: 사용된 출처 리스트
            
        Returns:
            검증 결과 (is_valid, warnings, errors)
        """
        warnings = []
        errors = []
        
        # 1. 출처 확인
        if not sources or len(sources) == 0:
            warnings.append("출처가 명시되지 않았습니다")
        
        # 2. 답변 길이 확인
        if len(answer) < 10:
            errors.append("답변이 너무 짧습니다")
        
        if len(answer) > 2000:
            warnings.append("답변이 너무 깁니다 (2000자 초과)")
        
        # 3. 추측성 표현 확인
        speculative_phrases = [
            "아마도", "추측", "~일 것", "~같습니다", "확실하지 않지만",
            "~인 것 같", "~로 보입니다", "예상", "짐작"
        ]
        
        for phrase in speculative_phrases:
            if phrase in answer:
                warnings.append(f"추측성 표현 발견: '{phrase}'")
        
        # 4. 금지 표현 확인
        prohibited_phrases = [
            "제가 판단하기에", "개인적으로", "~하는 게 좋을 것 같아요",
            "~하면 안 될 것 같아요"
        ]
        
        for phrase in prohibited_phrases:
            if phrase in answer:
                errors.append(f"금지된 표현 발견: '{phrase}'")
        
        # 5. 답변 구조 확인 (간단한 체크)
        has_summary = any(marker in answer for marker in ["요약", "한 줄", "핵심"])
        has_action_guide = any(marker in answer for marker in ["신청", "방법", "확인", "준비"])
        
        if not has_action_guide:
            warnings.append("행동 가이드가 명시적이지 않을 수 있습니다")
        
        # 검증 결과
        is_valid = len(errors) == 0
        
        return {
            "is_valid": is_valid,
            "warnings": warnings,
            "errors": errors,
            "answer_length": len(answer),
            "sources_count": len(sources) if sources else 0,
        }
    
    def fix_answer_if_needed(self, answer: str, validation_result: Dict[str, Any]) -> str:
        """
        검증 결과에 따라 답변 수정 (필요 시)
        
        Args:
            answer: 원본 답변
            validation_result: 검증 결과
            
        Returns:
            수정된 답변 (또는 원본)
        """
        if validation_result["is_valid"]:
            return answer
        
        # 에러가 있으면 수정 불가 - 에러 메시지 반환
        if validation_result["errors"]:
            logger.error(f"답변 검증 실패: {validation_result['errors']}")
            return answer
        
        # 경고만 있으면 원본 반환 (경고는 무시 가능)
        if validation_result["warnings"]:
            logger.warning(f"답변 검증 경고: {validation_result['warnings']}")
        
        return answer


def get_answer_validator() -> AnswerValidator:
    """답변 검증기 인스턴스 반환"""
    return AnswerValidator()

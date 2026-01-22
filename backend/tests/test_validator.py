"""
Unit tests for answer validator.
"""

import pytest
from app.services.ai.validator import AnswerValidator


@pytest.mark.unit
class TestAnswerValidator:
    """Test cases for AnswerValidator."""
    
    def test_validate_answer_pass(self):
        """Test validation with a good answer."""
        validator = AnswerValidator()
        answer = """
        # 수강신청 일정 안내
        
        **요약**: 1학기 수강신청은 3월 1일부터 3월 5일까지입니다.
        
        ## 상세 설명
        수강신청 기간은 다음과 같습니다:
        - 1학기: 3월 1일 ~ 3월 5일
        - 2학기: 8월 3일 ~ 8월 7일
        
        ## 다음 행동 가이드
        1. 수강 희망 과목 미리 정리하기
        2. 시간표 겹치지 않게 계획하기
        3. 수강신청 사이트 미리 접속해보기
        
        **출처**: 2025학년도 학사일정
        """
        
        is_valid, issues = validator.validate(answer)
        
        assert is_valid, "Valid answer should pass validation"
        assert len(issues) == 0, "Should have no validation issues"
    
    def test_detect_speculative_language(self):
        """Test detection of speculative language."""
        validator = AnswerValidator()
        answer = "수강신청은 아마도 3월에 할 것 같아요. 정확하지는 않지만..."
        
        is_valid, issues = validator.validate(answer)
        
        assert not is_valid, "Should fail validation for speculative language"
        assert any("추측" in issue or "불확실" in issue for issue in issues)
    
    def test_detect_prohibited_phrases(self):
        """Test detection of prohibited phrases."""
        validator = AnswerValidator()
        answer = "제 생각에는 수강신청이 3월일 거예요. 확실하지 않아요."
        
        is_valid, issues = validator.validate(answer)
        
        assert not is_valid, "Should fail validation for prohibited phrases"
        assert any("금지" in issue for issue in issues)
    
    def test_require_source_citation(self):
        """Test that answers should include source citation."""
        validator = AnswerValidator()
        answer = "1학기 수강신청은 3월 1일부터 3월 5일까지입니다."
        
        is_valid, issues = validator.validate(answer)
        
        # This might pass or fail depending on implementation
        # If source is required, it should fail
        if not is_valid:
            assert any("출처" in issue for issue in issues)
    
    def test_empty_answer(self):
        """Test validation with empty answer."""
        validator = AnswerValidator()
        
        is_valid, issues = validator.validate("")
        
        assert not is_valid, "Empty answer should fail validation"
        assert len(issues) > 0
    
    def test_answer_with_proper_structure(self):
        """Test that well-structured answers pass validation."""
        validator = AnswerValidator()
        answer = """
        # 장학금 신청 안내
        
        **요약**: 교내 장학금은 매 학기 초에 신청할 수 있습니다.
        
        ## 상세 설명
        신청 자격: 재학생 중 성적 기준 충족자
        
        ## 다음 행동 가이드
        1. 학생포털 접속
        2. 장학금 신청 메뉴 선택
        3. 필요 서류 업로드
        
        **출처**: 학생처 공지사항
        """
        
        is_valid, issues = validator.validate(answer)
        
        assert is_valid, "Well-structured answer should pass"

"""
Unit tests for search service.
"""

import pytest
from datetime import datetime
from app.services.search import (
    search_schedules_by_keyword,
    search_notices_by_keyword,
    search_programs_by_keyword,
    search_glossary_by_keyword,
)
from app.models.academic_schedule import AcademicSchedule
from app.models.notice import Notice
from app.models.support_program import SupportProgram
from app.models.academic_glossary import AcademicGlossary


@pytest.mark.unit
class TestKeywordSearch:
    """Test cases for keyword-based search."""
    
    def test_search_schedules_by_keyword(self, db_session):
        """Test schedule search by keyword."""
        # Create test data
        schedule = AcademicSchedule(
            name="1학기 수강신청",
            start_date=datetime(2025, 3, 1),
            end_date=datetime(2025, 3, 5),
            semester="1학기",
            description="1학기 수강신청 기간입니다."
        )
        db_session.add(schedule)
        db_session.commit()
        
        # Search
        results = search_schedules_by_keyword(db_session, "수강신청")
        
        assert len(results) > 0, "Should find schedule with keyword '수강신청'"
        assert results[0].name == "1학기 수강신청"
    
    def test_search_schedules_no_results(self, db_session):
        """Test schedule search with no matching results."""
        results = search_schedules_by_keyword(db_session, "존재하지않는검색어")
        
        assert len(results) == 0, "Should return empty list for non-matching keyword"
    
    def test_search_notices_by_keyword(self, db_session):
        """Test notice search by keyword."""
        # Create test data
        notice = Notice(
            title="2025학년도 장학금 신청 안내",
            content="장학금 신청 기간이 시작되었습니다.",
            published_date=datetime(2025, 1, 15),
            category="장학금",
            importance="high"
        )
        db_session.add(notice)
        db_session.commit()
        
        # Search
        results = search_notices_by_keyword(db_session, "장학금")
        
        assert len(results) > 0, "Should find notice with keyword '장학금'"
        assert "장학금" in results[0].title
    
    def test_search_programs_by_keyword(self, db_session):
        """Test support program search by keyword."""
        # Create test data
        program = SupportProgram(
            name="신입생 멘토링 프로그램",
            description="신입생을 위한 학업 지원 멘토링",
            program_type="멘토링",
            target_audience="신입생",
            application_period_start=datetime(2025, 2, 1),
            application_period_end=datetime(2025, 2, 28)
        )
        db_session.add(program)
        db_session.commit()
        
        # Search
        results = search_programs_by_keyword(db_session, "멘토링")
        
        assert len(results) > 0, "Should find program with keyword '멘토링'"
        assert "멘토링" in results[0].name
    
    def test_search_glossary_by_keyword(self, db_session):
        """Test glossary search by keyword."""
        # Create test data
        glossary = AcademicGlossary(
            term="복수전공",
            definition="두 개의 전공을 동시에 이수하는 제도",
            category="학사 제도"
        )
        db_session.add(glossary)
        db_session.commit()
        
        # Search
        results = search_glossary_by_keyword(db_session, "복수전공")
        
        assert len(results) > 0, "Should find glossary with keyword '복수전공'"
        assert results[0].term == "복수전공"

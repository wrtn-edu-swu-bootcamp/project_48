"""
Integration tests for Programs API endpoints.
"""

import pytest
from datetime import datetime
from app.models.support_program import SupportProgram


@pytest.mark.integration
class TestProgramsAPI:
    """Test cases for Programs API."""
    
    def test_get_programs_empty(self, client, db_session):
        """Test getting programs when database is empty."""
        response = client.get("/api/v1/programs")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0
    
    def test_get_programs_with_data(self, client, db_session):
        """Test getting programs with data in database."""
        # Create test programs
        programs = [
            SupportProgram(
                name="신입생 멘토링",
                description="신입생을 위한 학업 지원",
                program_type="멘토링",
                target_audience="신입생",
                application_period_start=datetime(2025, 2, 1),
                application_period_end=datetime(2025, 2, 28)
            ),
            SupportProgram(
                name="교내 장학금",
                description="성적 우수 장학금",
                program_type="장학금",
                target_audience="재학생",
                application_period_start=datetime(2025, 3, 1),
                application_period_end=datetime(2025, 3, 15)
            )
        ]
        for program in programs:
            db_session.add(program)
        db_session.commit()
        
        response = client.get("/api/v1/programs")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 2
    
    def test_get_programs_filter_by_type(self, client, db_session):
        """Test filtering programs by type."""
        # Create test programs
        programs = [
            SupportProgram(
                name="멘토링 프로그램",
                program_type="멘토링",
                target_audience="신입생",
                application_period_start=datetime(2025, 2, 1),
                application_period_end=datetime(2025, 2, 28)
            ),
            SupportProgram(
                name="장학금 프로그램",
                program_type="장학금",
                target_audience="재학생",
                application_period_start=datetime(2025, 3, 1),
                application_period_end=datetime(2025, 3, 15)
            )
        ]
        for program in programs:
            db_session.add(program)
        db_session.commit()
        
        response = client.get("/api/v1/programs?program_type=멘토링")
        
        assert response.status_code == 200
        data = response.json()
        assert all(item["program_type"] == "멘토링" for item in data)

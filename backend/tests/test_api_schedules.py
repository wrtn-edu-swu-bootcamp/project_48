"""
Integration tests for Schedules API endpoints.
"""

import pytest
from datetime import datetime
from app.models.academic_schedule import AcademicSchedule


@pytest.mark.integration
class TestSchedulesAPI:
    """Test cases for Schedules API."""
    
    def test_get_schedules_empty(self, client, db_session):
        """Test getting schedules when database is empty."""
        response = client.get("/api/v1/schedules")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0
    
    def test_get_schedules_with_data(self, client, db_session):
        """Test getting schedules with data in database."""
        # Create test schedules
        schedules = [
            AcademicSchedule(
                name="1학기 수강신청",
                start_date=datetime(2025, 3, 1),
                end_date=datetime(2025, 3, 5),
                semester="1학기",
                description="1학기 수강신청 기간"
            ),
            AcademicSchedule(
                name="2학기 수강신청",
                start_date=datetime(2025, 8, 3),
                end_date=datetime(2025, 8, 7),
                semester="2학기",
                description="2학기 수강신청 기간"
            )
        ]
        for schedule in schedules:
            db_session.add(schedule)
        db_session.commit()
        
        response = client.get("/api/v1/schedules")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 2
        assert any("수강신청" in item["name"] for item in data)
    
    def test_get_schedules_filter_by_semester(self, client, db_session):
        """Test filtering schedules by semester."""
        # Create test schedules
        schedules = [
            AcademicSchedule(
                name="1학기 수강신청",
                start_date=datetime(2025, 3, 1),
                end_date=datetime(2025, 3, 5),
                semester="1학기"
            ),
            AcademicSchedule(
                name="2학기 수강신청",
                start_date=datetime(2025, 8, 3),
                end_date=datetime(2025, 8, 7),
                semester="2학기"
            )
        ]
        for schedule in schedules:
            db_session.add(schedule)
        db_session.commit()
        
        response = client.get("/api/v1/schedules?semester=1학기")
        
        assert response.status_code == 200
        data = response.json()
        assert all(item["semester"] == "1학기" for item in data)

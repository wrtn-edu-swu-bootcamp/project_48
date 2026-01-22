"""
Integration tests for Notices API endpoints.
"""

import pytest
from datetime import datetime
from app.models.notice import Notice


@pytest.mark.integration
class TestNoticesAPI:
    """Test cases for Notices API."""
    
    def test_get_notices_empty(self, client, db_session):
        """Test getting notices when database is empty."""
        response = client.get("/api/v1/notices")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0
    
    def test_get_notices_with_data(self, client, db_session):
        """Test getting notices with data in database."""
        # Create test notices
        notices = [
            Notice(
                title="2025학년도 장학금 신청 안내",
                content="장학금 신청 기간이 시작되었습니다.",
                published_date=datetime(2025, 1, 15),
                category="장학금",
                importance="high"
            ),
            Notice(
                title="학사 일정 변경 안내",
                content="중간고사 일정이 변경되었습니다.",
                published_date=datetime(2025, 2, 1),
                category="학사",
                importance="medium"
            )
        ]
        for notice in notices:
            db_session.add(notice)
        db_session.commit()
        
        response = client.get("/api/v1/notices")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 2
    
    def test_get_notices_filter_by_category(self, client, db_session):
        """Test filtering notices by category."""
        # Create test notices
        notices = [
            Notice(
                title="장학금 공지",
                content="내용",
                published_date=datetime(2025, 1, 15),
                category="장학금"
            ),
            Notice(
                title="학사 공지",
                content="내용",
                published_date=datetime(2025, 1, 15),
                category="학사"
            )
        ]
        for notice in notices:
            db_session.add(notice)
        db_session.commit()
        
        response = client.get("/api/v1/notices?category=장학금")
        
        assert response.status_code == 200
        data = response.json()
        assert all(item["category"] == "장학금" for item in data)

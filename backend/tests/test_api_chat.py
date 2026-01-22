"""
Integration tests for Chat API endpoints.
"""

import pytest
from unittest.mock import patch, AsyncMock, Mock


@pytest.mark.integration
class TestChatAPI:
    """Test cases for Chat API."""
    
    def test_chat_endpoint_success(self, client):
        """Test successful chat request."""
        mock_result = {
            "answer": "# 수강신청 일정 안내\n\n1학기 수강신청은 3월 1일~5일입니다.",
            "sources": [
                {"title": "2025학년도 학사일정", "source_type": "academic_schedule"}
            ]
        }
        
        with patch('app.api.v1.chat.RAGPipeline.process_question', new_callable=AsyncMock) as mock_rag:
            mock_rag.return_value = mock_result
            
            response = client.post(
                "/api/v1/chat",
                json={"question": "수강신청은 언제 하나요?"}
            )
            
            assert response.status_code == 200
            data = response.json()
            assert "answer" in data
            assert "sources" in data
            assert len(data["answer"]) > 0
    
    def test_chat_endpoint_empty_question(self, client):
        """Test chat endpoint with empty question."""
        response = client.post(
            "/api/v1/chat",
            json={"question": ""}
        )
        
        # Should return 422 for validation error
        assert response.status_code == 422
    
    def test_chat_endpoint_invalid_json(self, client):
        """Test chat endpoint with invalid JSON."""
        response = client.post(
            "/api/v1/chat",
            data="invalid json"
        )
        
        assert response.status_code == 422
    
    def test_chat_endpoint_missing_question(self, client):
        """Test chat endpoint without question field."""
        response = client.post(
            "/api/v1/chat",
            json={}
        )
        
        assert response.status_code == 422
    
    def test_chat_endpoint_error_handling(self, client):
        """Test chat endpoint error handling."""
        with patch('app.api.v1.chat.RAGPipeline.process_question', side_effect=Exception("Test error")):
            response = client.post(
                "/api/v1/chat",
                json={"question": "수강신청은 언제 하나요?"}
            )
            
            # Should return 500 for server error
            assert response.status_code == 500
            data = response.json()
            assert "detail" in data
    
    def test_chat_endpoint_long_question(self, client):
        """Test chat endpoint with very long question."""
        long_question = "수강신청" * 200  # Very long question
        
        mock_result = {
            "answer": "질문이 너무 길어서 처리할 수 없습니다.",
            "sources": []
        }
        
        with patch('app.api.v1.chat.RAGPipeline.process_question', new_callable=AsyncMock) as mock_rag:
            mock_rag.return_value = mock_result
            
            response = client.post(
                "/api/v1/chat",
                json={"question": long_question}
            )
            
            # Should handle long questions gracefully
            assert response.status_code in [200, 400, 422]

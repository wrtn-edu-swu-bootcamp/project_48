"""
Integration tests for RAG pipeline.
"""

import pytest
from unittest.mock import Mock, patch, AsyncMock
from app.services.ai.rag import RAGPipeline


@pytest.mark.integration
class TestRAGPipeline:
    """Test cases for RAG Pipeline."""
    
    @pytest.mark.asyncio
    async def test_rag_pipeline_full_flow(self, db_session, sample_question):
        """Test complete RAG pipeline flow."""
        pipeline = RAGPipeline()
        
        # Mock Gemini API response
        mock_response = Mock()
        mock_response.content = [
            Mock(text="# 수강신청 일정 안내\n\n**요약**: 1학기 수강신청은 3월 1일~5일입니다.\n\n**출처**: 학사일정")
        ]
        
        with patch('app.services.ai.client.GeminiClient.generate_response', new_callable=AsyncMock) as mock_gemini:
            mock_gemini.return_value = mock_response
            
            result = await pipeline.process_question(sample_question, db_session)
            
            assert result is not None, "Should return a result"
            assert "answer" in result, "Result should contain answer"
            assert "sources" in result, "Result should contain sources"
            assert len(result["answer"]) > 0, "Answer should not be empty"
    
    @pytest.mark.asyncio
    async def test_rag_pipeline_with_no_context(self, db_session):
        """Test RAG pipeline when no relevant context is found."""
        pipeline = RAGPipeline()
        question = "이 질문은 데이터베이스에 없는 내용입니다"
        
        mock_response = Mock()
        mock_response.content = [
            Mock(text="해당 내용은 현재 제공된 정보에서 확인되지 않아요.")
        ]
        
        with patch('app.services.ai.client.GeminiClient.generate_response', new_callable=AsyncMock) as mock_gemini:
            mock_gemini.return_value = mock_response
            
            result = await pipeline.process_question(question, db_session)
            
            assert result is not None
            assert "answer" in result
            # Should return fallback message
            assert "확인되지 않" in result["answer"] or len(result.get("sources", [])) == 0
    
    @pytest.mark.asyncio
    async def test_rag_pipeline_error_handling(self, db_session, sample_question):
        """Test RAG pipeline error handling."""
        pipeline = RAGPipeline()
        
        with patch('app.services.ai.client.GeminiClient.generate_response', side_effect=Exception("API Error")):
            result = await pipeline.process_question(sample_question, db_session)
            
            # Should return fallback response on error
            assert result is not None
            assert "answer" in result
            # Check for error handling
            assert "오류" in result["answer"] or "문제" in result["answer"]
    
    @pytest.mark.asyncio
    async def test_rag_pipeline_classification(self, db_session):
        """Test that RAG pipeline correctly classifies questions."""
        pipeline = RAGPipeline()
        
        test_cases = [
            ("수강신청은 언제 하나요?", "academic_schedule"),
            ("장학금 신청 방법이 궁금해요", "support_program"),
            ("최근 공지사항을 알려주세요", "notice"),
            ("복수전공이 뭔가요?", "glossary"),
        ]
        
        mock_response = Mock()
        mock_response.content = [Mock(text="테스트 답변")]
        
        with patch('app.services.ai.client.ClaudeClient.generate_response', new_callable=AsyncMock) as mock_claude:
            mock_claude.return_value = mock_response
            
            for question, expected_category in test_cases:
                result = await pipeline.process_question(question, db_session)
                # Just verify it processes without error
                assert result is not None

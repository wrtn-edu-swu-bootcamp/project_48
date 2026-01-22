"""
Unit tests for embedding service.
"""

import pytest
import numpy as np
from app.services.ai.embeddings import EmbeddingService


@pytest.mark.unit
class TestEmbeddingService:
    """Test cases for EmbeddingService."""
    
    def test_singleton_pattern(self):
        """Test that EmbeddingService follows singleton pattern."""
        service1 = EmbeddingService()
        service2 = EmbeddingService()
        assert service1 is service2, "EmbeddingService should be a singleton"
    
    def test_generate_embedding_single(self):
        """Test single text embedding generation."""
        service = EmbeddingService()
        text = "수강신청은 언제 하나요?"
        
        embedding = service.generate_embedding(text)
        
        assert embedding is not None, "Embedding should not be None"
        assert isinstance(embedding, list), "Embedding should be a list"
        assert len(embedding) == 384, "Embedding dimension should be 384"
        assert all(isinstance(x, float) for x in embedding), "All values should be floats"
    
    def test_generate_embedding_empty_text(self):
        """Test embedding generation with empty text."""
        service = EmbeddingService()
        
        embedding = service.generate_embedding("")
        
        assert embedding is not None, "Should handle empty text"
        assert len(embedding) == 384, "Should return 384-dim vector even for empty text"
    
    def test_generate_embeddings_batch(self):
        """Test batch embedding generation."""
        service = EmbeddingService()
        texts = [
            "수강신청은 언제 하나요?",
            "장학금 신청 방법이 궁금해요",
            "학사 일정을 알려주세요"
        ]
        
        embeddings = service.generate_embeddings(texts)
        
        assert len(embeddings) == 3, "Should return 3 embeddings"
        assert all(len(emb) == 384 for emb in embeddings), "All embeddings should be 384-dim"
    
    def test_embedding_similarity(self):
        """Test that similar texts produce similar embeddings."""
        service = EmbeddingService()
        
        text1 = "수강신청은 언제 하나요?"
        text2 = "수강신청 일정이 궁금해요"
        text3 = "학교 위치가 어디인가요?"
        
        emb1 = np.array(service.generate_embedding(text1))
        emb2 = np.array(service.generate_embedding(text2))
        emb3 = np.array(service.generate_embedding(text3))
        
        # Cosine similarity
        similarity_12 = np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))
        similarity_13 = np.dot(emb1, emb3) / (np.linalg.norm(emb1) * np.linalg.norm(emb3))
        
        assert similarity_12 > similarity_13, "Similar texts should have higher similarity"

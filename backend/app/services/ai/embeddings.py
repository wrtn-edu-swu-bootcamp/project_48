"""
임베딩 서비스
sentence-transformers를 사용한 텍스트 임베딩 생성 (캐싱 및 배치 처리 최적화)
"""
from typing import List, Optional
import numpy as np
from sentence_transformers import SentenceTransformer
import json
import logging
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache

logger = logging.getLogger(__name__)

class EmbeddingService:
    """텍스트 임베딩 생성 서비스 (캐싱 및 배치 처리 최적화)"""
    
    def __init__(self, model_name: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"):
        """
        임베딩 서비스 초기화
        
        Args:
            model_name: 사용할 sentence-transformers 모델명
        """
        self.model_name = model_name
        self.model: Optional[SentenceTransformer] = None
        self.embedding_dimension = 384  # MiniLM-L12-v2의 차원
        self._cache = None  # 캐시 서비스 (지연 로딩)
        self._executor = ThreadPoolExecutor(max_workers=4)  # 병렬 처리용
        
    def _get_cache(self):
        """캐시 서비스 가져오기 (지연 로딩)"""
        if self._cache is None:
            try:
                from app.core.cache import get_cache_service
                self._cache = get_cache_service()
            except Exception as e:
                logger.warning(f"캐시 서비스 로드 실패: {e}")
                self._cache = None
        return self._cache
    
    def load_model(self):
        """모델 로드 (지연 로딩)"""
        if self.model is None:
            logger.info(f"임베딩 모델 로드 중: {self.model_name}")
            self.model = SentenceTransformer(self.model_name)
            logger.info(f"✓ 임베딩 모델 로드 완료")
    
    def get_embedding(self, text: str, use_cache: bool = True) -> List[float]:
        """
        텍스트를 벡터로 변환 (캐싱 지원)
        
        Args:
            text: 임베딩할 텍스트
            use_cache: 캐시 사용 여부
            
        Returns:
            384차원 벡터 (리스트)
        """
        if not text or not text.strip():
            # 빈 텍스트의 경우 제로 벡터 반환
            return [0.0] * self.embedding_dimension
        
        # 캐시 확인
        if use_cache:
            cache = self._get_cache()
            if cache:
                cached_embedding = cache.get_embedding(text)
                if cached_embedding:
                    logger.debug(f"임베딩 캐시 히트: {text[:50]}...")
                    return cached_embedding
        
        self.load_model()
        
        # 임베딩 생성
        embedding = self.model.encode(text, convert_to_numpy=True)
        embedding_list = embedding.tolist()
        
        # 캐시 저장
        if use_cache:
            cache = self._get_cache()
            if cache:
                cache.set_embedding(text, embedding_list)
        
        return embedding_list
    
    def get_embeddings_batch(self, texts: List[str], use_cache: bool = True, batch_size: int = 32) -> List[List[float]]:
        """
        여러 텍스트를 한 번에 벡터로 변환 (배치 처리 + 캐싱 최적화)
        
        Args:
            texts: 임베딩할 텍스트 리스트
            use_cache: 캐시 사용 여부
            batch_size: 배치 크기
            
        Returns:
            벡터 리스트
        """
        if not texts:
            return []
        
        results = []
        texts_to_encode = []
        text_indices = []
        
        # 캐시 확인 및 미싱 텍스트 수집
        cache = self._get_cache() if use_cache else None
        
        for i, text in enumerate(texts):
            if not text or not text.strip():
                results.append([0.0] * self.embedding_dimension)
                continue
            
            # 캐시 확인
            if cache:
                cached_embedding = cache.get_embedding(text)
                if cached_embedding:
                    results.append(cached_embedding)
                    continue
            
            # 캐시 미스 - 인코딩 대상에 추가
            texts_to_encode.append(text)
            text_indices.append(i)
            results.append(None)  # 플레이스홀더
        
        # 캐시되지 않은 텍스트만 인코딩
        if texts_to_encode:
            logger.info(f"임베딩 생성: {len(texts_to_encode)}/{len(texts)}개 (캐시 히트: {len(texts) - len(texts_to_encode)}개)")
            self.load_model()
            
            # 배치 임베딩 생성
            embeddings = self.model.encode(
                texts_to_encode, 
                convert_to_numpy=True, 
                batch_size=batch_size,
                show_progress_bar=len(texts_to_encode) > 100  # 100개 이상일 때만 진행률 표시
            )
            
            # 결과 저장 및 캐시 업데이트
            for idx, embedding in zip(text_indices, embeddings):
                embedding_list = embedding.tolist()
                results[idx] = embedding_list
                
                # 캐시 저장
                if cache:
                    cache.set_embedding(texts[idx], embedding_list)
        
        return results
    
    def compute_similarity(self, embedding1: List[float], embedding2: List[float]) -> float:
        """
        두 임베딩 간의 코사인 유사도 계산
        
        Args:
            embedding1: 첫 번째 임베딩
            embedding2: 두 번째 임베딩
            
        Returns:
            코사인 유사도 (0~1)
        """
        vec1 = np.array(embedding1)
        vec2 = np.array(embedding2)
        
        # 코사인 유사도 계산
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        similarity = dot_product / (norm1 * norm2)
        
        # -1 ~ 1 범위를 0 ~ 1 범위로 변환
        return (similarity + 1) / 2
    
    def embedding_to_db_format(self, embedding: List[float]) -> str:
        """
        임베딩을 데이터베이스 저장 형식으로 변환
        PostgreSQL의 pgvector는 벡터를 직접 받지만, SQLite는 JSON 문자열로 저장
        
        Args:
            embedding: 임베딩 벡터
            
        Returns:
            JSON 문자열 (SQLite용) 또는 벡터 그대로 (PostgreSQL용)
        """
        # SQLite는 JSON 문자열로 저장
        return json.dumps(embedding)
    
    def db_format_to_embedding(self, db_value: str) -> List[float]:
        """
        데이터베이스 형식을 임베딩 벡터로 변환
        
        Args:
            db_value: 데이터베이스 저장 값
            
        Returns:
            임베딩 벡터
        """
        if isinstance(db_value, str):
            # SQLite에서 JSON 문자열로 저장된 경우
            return json.loads(db_value)
        else:
            # PostgreSQL에서 벡터로 저장된 경우
            return db_value


# 전역 임베딩 서비스 인스턴스
_embedding_service: Optional[EmbeddingService] = None


def get_embedding_service() -> EmbeddingService:
    """임베딩 서비스 싱글톤 인스턴스 반환"""
    global _embedding_service
    if _embedding_service is None:
        from app.core.config import settings
        _embedding_service = EmbeddingService(model_name=settings.EMBEDDING_MODEL)
    return _embedding_service

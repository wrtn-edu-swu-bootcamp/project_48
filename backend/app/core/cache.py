"""
Redis 캐싱 서비스
"""
import json
import hashlib
from typing import Any, Optional
from redis import Redis
from redis.exceptions import RedisError
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


class CacheService:
    """Redis 기반 캐싱 서비스"""
    
    def __init__(self):
        """캐시 서비스 초기화"""
        self._client: Optional[Redis] = None
        self._enabled = settings.REDIS_ENABLED
        
        if self._enabled:
            try:
                self._client = Redis.from_url(
                    settings.REDIS_URL,
                    decode_responses=True,
                    socket_connect_timeout=5,
                    socket_keepalive=True,
                    health_check_interval=30,
                )
                # 연결 테스트
                self._client.ping()
                logger.info("Redis 캐시 연결 성공")
            except RedisError as e:
                logger.warning(f"Redis 연결 실패, 캐싱 비활성화: {e}")
                self._enabled = False
                self._client = None
    
    def _make_key(self, prefix: str, key: str) -> str:
        """캐시 키 생성"""
        return f"{prefix}:{key}"
    
    def _hash_key(self, data: Any) -> str:
        """데이터를 해시하여 키 생성"""
        if isinstance(data, (dict, list)):
            data_str = json.dumps(data, sort_keys=True, ensure_ascii=False)
        else:
            data_str = str(data)
        return hashlib.sha256(data_str.encode()).hexdigest()[:16]
    
    def get(self, prefix: str, key: str) -> Optional[Any]:
        """캐시에서 값 가져오기"""
        if not self._enabled or not self._client:
            return None
        
        try:
            cache_key = self._make_key(prefix, key)
            value = self._client.get(cache_key)
            if value:
                logger.debug(f"캐시 히트: {cache_key}")
                return json.loads(value)
            logger.debug(f"캐시 미스: {cache_key}")
            return None
        except (RedisError, json.JSONDecodeError) as e:
            logger.error(f"캐시 읽기 오류: {e}")
            return None
    
    def set(self, prefix: str, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """캐시에 값 저장"""
        if not self._enabled or not self._client:
            return False
        
        try:
            cache_key = self._make_key(prefix, key)
            value_json = json.dumps(value, ensure_ascii=False)
            
            if ttl:
                self._client.setex(cache_key, ttl, value_json)
            else:
                self._client.set(cache_key, value_json)
            
            logger.debug(f"캐시 저장: {cache_key} (TTL: {ttl}s)")
            return True
        except (RedisError, TypeError, ValueError) as e:
            logger.error(f"캐시 저장 오류: {e}")
            return False
    
    def delete(self, prefix: str, key: str) -> bool:
        """캐시에서 값 삭제"""
        if not self._enabled or not self._client:
            return False
        
        try:
            cache_key = self._make_key(prefix, key)
            self._client.delete(cache_key)
            logger.debug(f"캐시 삭제: {cache_key}")
            return True
        except RedisError as e:
            logger.error(f"캐시 삭제 오류: {e}")
            return False
    
    def clear_prefix(self, prefix: str) -> int:
        """특정 프리픽스의 모든 캐시 삭제"""
        if not self._enabled or not self._client:
            return 0
        
        try:
            pattern = f"{prefix}:*"
            keys = self._client.keys(pattern)
            if keys:
                deleted = self._client.delete(*keys)
                logger.info(f"캐시 삭제: {deleted}개 ({prefix}:*)")
                return deleted
            return 0
        except RedisError as e:
            logger.error(f"캐시 일괄 삭제 오류: {e}")
            return 0
    
    def get_embedding(self, text: str) -> Optional[list]:
        """임베딩 캐시 조회"""
        key = self._hash_key(text)
        return self.get("embedding", key)
    
    def set_embedding(self, text: str, embedding: list) -> bool:
        """임베딩 캐시 저장"""
        key = self._hash_key(text)
        return self.set("embedding", key, embedding, settings.CACHE_TTL_EMBEDDING)
    
    def get_search_result(self, query: str, filters: Optional[dict] = None) -> Optional[Any]:
        """검색 결과 캐시 조회"""
        key_data = {"query": query, "filters": filters or {}}
        key = self._hash_key(key_data)
        return self.get("search", key)
    
    def set_search_result(self, query: str, result: Any, filters: Optional[dict] = None) -> bool:
        """검색 결과 캐시 저장"""
        key_data = {"query": query, "filters": filters or {}}
        key = self._hash_key(key_data)
        return self.set("search", key, result, settings.CACHE_TTL_SEARCH)
    
    def get_api_response(self, endpoint: str, params: Optional[dict] = None) -> Optional[Any]:
        """API 응답 캐시 조회"""
        key_data = {"endpoint": endpoint, "params": params or {}}
        key = self._hash_key(key_data)
        return self.get("api", key)
    
    def set_api_response(self, endpoint: str, response: Any, params: Optional[dict] = None) -> bool:
        """API 응답 캐시 저장"""
        key_data = {"endpoint": endpoint, "params": params or {}}
        key = self._hash_key(key_data)
        return self.set("api", key, response, settings.CACHE_TTL_API)
    
    def healthcheck(self) -> bool:
        """Redis 연결 상태 확인"""
        if not self._enabled or not self._client:
            return False
        
        try:
            return self._client.ping()
        except RedisError:
            return False


# 싱글톤 인스턴스
_cache_service: Optional[CacheService] = None


def get_cache_service() -> CacheService:
    """캐시 서비스 싱글톤 인스턴스 반환"""
    global _cache_service
    if _cache_service is None:
        _cache_service = CacheService()
    return _cache_service

"""
검색 서비스 (캐싱 및 쿼리 최적화)
"""
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, text
from app.models.question_log import QuestionCategory
from app.models.academic_schedule import AcademicSchedule
from app.models.notice import Notice
from app.models.support_program import SupportProgram
from app.models.academic_glossary import AcademicGlossary
from app.services.ai.embeddings import get_embedding_service
from typing import List, Dict, Any, Optional
from datetime import date
import logging

logger = logging.getLogger(__name__)


class SearchService:
    """검색 서비스 (캐싱 최적화)"""
    
    def __init__(self, db: Session):
        self.db = db
        self.embedding_service = get_embedding_service()
        self._cache = None  # 캐시 서비스 (지연 로딩)
    
    def _get_cache(self):
        """캐시 서비스 가져오기"""
        if self._cache is None:
            try:
                from app.core.cache import get_cache_service
                self._cache = get_cache_service()
            except Exception as e:
                logger.warning(f"캐시 서비스 로드 실패: {e}")
                self._cache = None
        return self._cache
    
    def search_by_vector(
        self,
        query: str,
        category: Optional[QuestionCategory] = None,
        limit: int = 5,
        use_cache: bool = True,
    ) -> List[Dict[str, Any]]:
        """
        벡터 기반 의미 검색 (캐싱 지원)
        
        Args:
            query: 검색 쿼리
            category: 질문 카테고리 (선택)
            limit: 최대 결과 수
            use_cache: 캐시 사용 여부
            
        Returns:
            검색 결과 리스트
        """
        # 캐시 확인
        if use_cache:
            cache = self._get_cache()
            if cache:
                filters = {"category": category.value if category else None, "limit": limit}
                cached_result = cache.get_search_result(query, filters)
                if cached_result:
                    logger.debug(f"검색 캐시 히트: {query}")
                    return cached_result
        
        try:
            # 쿼리를 벡터로 변환 (캐싱 활성화)
            query_embedding = self.embedding_service.get_embedding(query, use_cache=use_cache)
            query_vector_str = str(query_embedding)
            
            results: List[Dict[str, Any]] = []
            
            if category is None or category == QuestionCategory.ACADEMIC_SCHEDULE:
                results.extend(self._vector_search_schedules(query_vector_str, limit))
            
            if category is None or category == QuestionCategory.NOTICE:
                results.extend(self._vector_search_notices(query_vector_str, limit))
            
            if category is None or category == QuestionCategory.SUPPORT_PROGRAM:
                results.extend(self._vector_search_programs(query_vector_str, limit))
            
            if category is None or category == QuestionCategory.ACADEMIC_INFO:
                results.extend(self._vector_search_glossary(query_vector_str, limit))
            
            # 유사도 점수로 정렬
            results.sort(key=lambda x: x.get("similarity", 0), reverse=True)
            final_results = results[:limit]
            
            # 결과 캐싱
            if use_cache:
                cache = self._get_cache()
                if cache:
                    filters = {"category": category.value if category else None, "limit": limit}
                    cache.set_search_result(query, final_results, filters)
            
            return final_results
            
        except Exception as e:
            logger.error(f"벡터 검색 중 오류: {e}")
            # 폴백: 키워드 검색
            return self.search(query, category or QuestionCategory.ACADEMIC_INFO, limit, use_cache=False)
    
    def hybrid_search(
        self,
        query: str,
        category: Optional[QuestionCategory] = None,
        limit: int = 5,
        use_cache: bool = True,
    ) -> List[Dict[str, Any]]:
        """
        하이브리드 검색 (키워드 + 벡터, 캐싱 지원)
        
        Args:
            query: 검색 쿼리
            category: 질문 카테고리 (선택)
            limit: 최대 결과 수
            use_cache: 캐시 사용 여부
            
        Returns:
            검색 결과 리스트
        """
        # 캐시 확인
        if use_cache:
            cache = self._get_cache()
            if cache:
                filters = {"category": category.value if category else None, "limit": limit, "hybrid": True}
                cached_result = cache.get_search_result(query, filters)
                if cached_result:
                    logger.debug(f"하이브리드 검색 캐시 히트: {query}")
                    return cached_result
        
        # 키워드 검색
        keyword_results = self.search(query, category or QuestionCategory.ACADEMIC_INFO, limit * 2, use_cache=False)
        
        # 벡터 검색
        vector_results = self.search_by_vector(query, category, limit * 2, use_cache=use_cache)
        
        # 결과 통합 (ID 기반 중복 제거)
        combined_results = {}
        
        for result in keyword_results:
            key = f"{result.get('source')}_{result.get('id')}"
            combined_results[key] = result
            combined_results[key]['keyword_score'] = result.get('relevance_score', 0)
            combined_results[key]['vector_score'] = 0
        
        for result in vector_results:
            key = f"{result.get('source')}_{result.get('id')}"
            if key in combined_results:
                combined_results[key]['vector_score'] = result.get('similarity', 0)
            else:
                combined_results[key] = result
                combined_results[key]['keyword_score'] = 0
                combined_results[key]['vector_score'] = result.get('similarity', 0)
        
        # 최종 점수 계산 (키워드 40% + 벡터 60%)
        for key in combined_results:
            result = combined_results[key]
            keyword_normalized = result.get('keyword_score', 0) / 10  # 0-1 범위로 정규화
            vector_normalized = result.get('vector_score', 0)  # 이미 0-1 범위
            result['final_score'] = (keyword_normalized * 0.4) + (vector_normalized * 0.6)
        
        # 최종 점수로 정렬
        final_results = list(combined_results.values())
        final_results.sort(key=lambda x: x.get('final_score', 0), reverse=True)
        final_results = final_results[:limit]
        
        # 결과 캐싱
        if use_cache:
            cache = self._get_cache()
            if cache:
                filters = {"category": category.value if category else None, "limit": limit, "hybrid": True}
                cache.set_search_result(query, final_results, filters)
        
        return final_results
    
    def search(
        self,
        query: str,
        category: QuestionCategory,
        limit: int = 5,
        use_cache: bool = True,
    ) -> List[Dict[str, Any]]:
        """
        질문과 카테고리에 맞는 정보를 검색합니다. (캐싱 지원)
        
        Args:
            query: 검색 쿼리
            category: 질문 카테고리
            limit: 최대 결과 수
            use_cache: 캐시 사용 여부
            
        Returns:
            검색 결과 리스트
        """
        # 캐시 확인
        if use_cache:
            cache = self._get_cache()
            if cache:
                filters = {"category": category.value, "limit": limit, "keyword": True}
                cached_result = cache.get_search_result(query, filters)
                if cached_result:
                    logger.debug(f"키워드 검색 캐시 히트: {query}")
                    return cached_result
        
        results: List[Dict[str, Any]] = []
        
        if category == QuestionCategory.ACADEMIC_SCHEDULE:
            results.extend(self._search_schedules(query, limit))
        elif category == QuestionCategory.NOTICE:
            results.extend(self._search_notices(query, limit))
        elif category == QuestionCategory.SUPPORT_PROGRAM:
            results.extend(self._search_programs(query, limit))
        elif category == QuestionCategory.ACADEMIC_INFO:
            results.extend(self._search_terms(query, limit))
        else:
            # 모든 카테고리에서 검색
            results.extend(self._search_schedules(query, limit // 4))
            results.extend(self._search_notices(query, limit // 4))
            results.extend(self._search_programs(query, limit // 4))
            results.extend(self._search_terms(query, limit // 4))
        
        # 관련성 점수로 정렬
        results.sort(key=lambda x: x.get("relevance_score", 0), reverse=True)
        final_results = results[:limit]
        
        # 결과 캐싱
        if use_cache:
            cache = self._get_cache()
            if cache:
                filters = {"category": category.value, "limit": limit, "keyword": True}
                cache.set_search_result(query, final_results, filters)
        
        return final_results
    
    def _search_schedules(self, query: str, limit: int) -> List[Dict[str, Any]]:
        """학사 일정 검색"""
        schedules = (
            self.db.query(AcademicSchedule)
            .filter(
                or_(
                    AcademicSchedule.name.ilike(f"%{query}%"),
                    AcademicSchedule.description.ilike(f"%{query}%"),
                )
            )
            .order_by(AcademicSchedule.importance.desc(), AcademicSchedule.start_date.desc())
            .limit(limit)
            .all()
        )
        
        return [
            {
                "id": schedule.id,
                "name": schedule.name,
                "description": schedule.description,
                "start_date": schedule.start_date.isoformat() if schedule.start_date else None,
                "end_date": schedule.end_date.isoformat() if schedule.end_date else None,
                "source": f"{schedule.semester.value} 학사일정",
                "relevance_score": self._calculate_relevance(query, schedule.name, schedule.description),
            }
            for schedule in schedules
        ]
    
    def _search_notices(self, query: str, limit: int) -> List[Dict[str, Any]]:
        """공지사항 검색"""
        notices = (
            self.db.query(Notice)
            .filter(
                and_(
                    Notice.is_active == 1,
                    or_(
                        Notice.title.ilike(f"%{query}%"),
                        Notice.content.ilike(f"%{query}%"),
                    ),
                )
            )
            .order_by(Notice.importance.desc(), Notice.created_at.desc())
            .limit(limit)
            .all()
        )
        
        return [
            {
                "id": notice.id,
                "title": notice.title,
                "content": notice.content,
                "source": f"{notice.notice_type.value} 공지사항",
                "relevance_score": self._calculate_relevance(query, notice.title, notice.content),
            }
            for notice in notices
        ]
    
    def _search_programs(self, query: str, limit: int) -> List[Dict[str, Any]]:
        """지원 프로그램 검색"""
        programs = (
            self.db.query(SupportProgram)
            .filter(
                and_(
                    SupportProgram.is_active == 1,
                    or_(
                        SupportProgram.name.ilike(f"%{query}%"),
                        SupportProgram.description.ilike(f"%{query}%"),
                    ),
                )
            )
            .order_by(SupportProgram.created_at.desc())
            .limit(limit)
            .all()
        )
        
        return [
            {
                "id": program.id,
                "name": program.name,
                "description": program.description,
                "application_method": program.application_method,
                "source": f"{program.program_type.value} 프로그램",
                "relevance_score": self._calculate_relevance(query, program.name, program.description),
            }
            for program in programs
        ]
    
    def _search_terms(self, query: str, limit: int) -> List[Dict[str, Any]]:
        """학사 용어 검색"""
        from app.models.academic_glossary import AcademicGlossary
        
        terms = (
            self.db.query(AcademicGlossary)
            .filter(
                or_(
                    AcademicGlossary.term_ko.ilike(f"%{query}%"),
                    AcademicGlossary.definition.ilike(f"%{query}%"),
                )
            )
            .limit(limit)
            .all()
        )
        
        return [
            {
                "id": term.id,
                "term": term.term_ko,
                "definition": term.definition,
                "examples": term.examples,
                "source": "학사 용어 사전",
                "relevance_score": self._calculate_relevance(query, term.term_ko, term.definition),
            }
            for term in terms
        ]
    
    def _vector_search_schedules(self, query_vector: str, limit: int) -> List[Dict[str, Any]]:
        """벡터 기반 학사 일정 검색"""
        # 데이터베이스 타입 확인
        bind = self.db.get_bind()
        is_postgresql = bind.dialect.name == 'postgresql'
        
        if is_postgresql:
            query = text(f"""
                SELECT id, name, description, start_date, end_date, semester,
                       1 - (embedding <=> '{query_vector}'::vector) as similarity
                FROM academic_schedules
                WHERE embedding IS NOT NULL
                ORDER BY embedding <=> '{query_vector}'::vector
                LIMIT :limit
            """)
        else:
            # SQLite는 벡터 검색을 지원하지 않으므로 모든 레코드를 가져와서 Python에서 계산
            schedules = self.db.query(AcademicSchedule).filter(
                AcademicSchedule.embedding.isnot(None)
            ).all()
            
            import json
            query_embedding = json.loads(query_vector) if isinstance(query_vector, str) else query_vector
            
            results = []
            for schedule in schedules:
                if schedule.embedding:
                    embedding = json.loads(schedule.embedding) if isinstance(schedule.embedding, str) else schedule.embedding
                    similarity = self.embedding_service.compute_similarity(query_embedding, embedding)
                    results.append({
                        "id": schedule.id,
                        "name": schedule.name,
                        "description": schedule.description,
                        "start_date": schedule.start_date.isoformat() if schedule.start_date else None,
                        "end_date": schedule.end_date.isoformat() if schedule.end_date else None,
                        "source": f"{schedule.semester.value} 학사일정",
                        "similarity": similarity,
                    })
            
            # 유사도로 정렬
            results.sort(key=lambda x: x["similarity"], reverse=True)
            return results[:limit]
        
        results = self.db.execute(query, {"limit": limit}).fetchall()
        
        return [
            {
                "id": row[0],
                "name": row[1],
                "description": row[2],
                "start_date": row[3].isoformat() if row[3] else None,
                "end_date": row[4].isoformat() if row[4] else None,
                "source": f"{row[5]} 학사일정",
                "similarity": float(row[6]),
            }
            for row in results
        ]
    
    def _vector_search_notices(self, query_vector: str, limit: int) -> List[Dict[str, Any]]:
        """벡터 기반 공지사항 검색"""
        bind = self.db.get_bind()
        is_postgresql = bind.dialect.name == 'postgresql'
        
        if is_postgresql:
            query = text(f"""
                SELECT id, title, content, notice_type,
                       1 - (embedding <=> '{query_vector}'::vector) as similarity
                FROM notices
                WHERE embedding IS NOT NULL AND is_active = 1
                ORDER BY embedding <=> '{query_vector}'::vector
                LIMIT :limit
            """)
            results = self.db.execute(query, {"limit": limit}).fetchall()
            
            return [
                {
                    "id": row[0],
                    "title": row[1],
                    "content": row[2],
                    "source": f"{row[3]} 공지사항",
                    "similarity": float(row[4]),
                }
                for row in results
            ]
        else:
            # SQLite: Python에서 유사도 계산
            notices = self.db.query(Notice).filter(
                Notice.embedding.isnot(None),
                Notice.is_active == 1
            ).all()
            
            import json
            query_embedding = json.loads(query_vector) if isinstance(query_vector, str) else query_vector
            
            results = []
            for notice in notices:
                if notice.embedding:
                    embedding = json.loads(notice.embedding) if isinstance(notice.embedding, str) else notice.embedding
                    similarity = self.embedding_service.compute_similarity(query_embedding, embedding)
                    results.append({
                        "id": notice.id,
                        "title": notice.title,
                        "content": notice.content,
                        "source": f"{notice.notice_type.value} 공지사항",
                        "similarity": similarity,
                    })
            
            results.sort(key=lambda x: x["similarity"], reverse=True)
            return results[:limit]
    
    def _vector_search_programs(self, query_vector: str, limit: int) -> List[Dict[str, Any]]:
        """벡터 기반 지원 프로그램 검색"""
        bind = self.db.get_bind()
        is_postgresql = bind.dialect.name == 'postgresql'
        
        if is_postgresql:
            query = text(f"""
                SELECT id, name, description, application_method, program_type,
                       1 - (embedding <=> '{query_vector}'::vector) as similarity
                FROM support_programs
                WHERE embedding IS NOT NULL AND is_active = 1
                ORDER BY embedding <=> '{query_vector}'::vector
                LIMIT :limit
            """)
            results = self.db.execute(query, {"limit": limit}).fetchall()
            
            return [
                {
                    "id": row[0],
                    "name": row[1],
                    "description": row[2],
                    "application_method": row[3],
                    "source": f"{row[4]} 프로그램",
                    "similarity": float(row[5]),
                }
                for row in results
            ]
        else:
            programs = self.db.query(SupportProgram).filter(
                SupportProgram.embedding.isnot(None),
                SupportProgram.is_active == 1
            ).all()
            
            import json
            query_embedding = json.loads(query_vector) if isinstance(query_vector, str) else query_vector
            
            results = []
            for program in programs:
                if program.embedding:
                    embedding = json.loads(program.embedding) if isinstance(program.embedding, str) else program.embedding
                    similarity = self.embedding_service.compute_similarity(query_embedding, embedding)
                    results.append({
                        "id": program.id,
                        "name": program.name,
                        "description": program.description,
                        "application_method": program.application_method,
                        "source": f"{program.program_type.value} 프로그램",
                        "similarity": similarity,
                    })
            
            results.sort(key=lambda x: x["similarity"], reverse=True)
            return results[:limit]
    
    def _vector_search_glossary(self, query_vector: str, limit: int) -> List[Dict[str, Any]]:
        """벡터 기반 학사 용어 검색"""
        bind = self.db.get_bind()
        is_postgresql = bind.dialect.name == 'postgresql'
        
        if is_postgresql:
            query = text(f"""
                SELECT id, term_ko, definition, examples,
                       1 - (embedding <=> '{query_vector}'::vector) as similarity
                FROM academic_glossary
                WHERE embedding IS NOT NULL
                ORDER BY embedding <=> '{query_vector}'::vector
                LIMIT :limit
            """)
            results = self.db.execute(query, {"limit": limit}).fetchall()
            
            return [
                {
                    "id": row[0],
                    "term": row[1],
                    "definition": row[2],
                    "examples": row[3],
                    "source": "학사 용어 사전",
                    "similarity": float(row[4]),
                }
                for row in results
            ]
        else:
            terms = self.db.query(AcademicGlossary).filter(
                AcademicGlossary.embedding.isnot(None)
            ).all()
            
            import json
            query_embedding = json.loads(query_vector) if isinstance(query_vector, str) else query_vector
            
            results = []
            for term in terms:
                if term.embedding:
                    embedding = json.loads(term.embedding) if isinstance(term.embedding, str) else term.embedding
                    similarity = self.embedding_service.compute_similarity(query_embedding, embedding)
                    results.append({
                        "id": term.id,
                        "term": term.term_ko,
                        "definition": term.definition,
                        "examples": term.examples,
                        "source": "학사 용어 사전",
                        "similarity": similarity,
                    })
            
            results.sort(key=lambda x: x["similarity"], reverse=True)
            return results[:limit]
    
    def _calculate_relevance(self, query: str, *texts: str) -> int:
        """관련성 점수 계산 (간단한 키워드 매칭 개수)"""
        query_lower = query.lower()
        score = 0
        
        for text in texts:
            if text:
                text_lower = text.lower()
                # 키워드가 포함된 횟수 계산
                score += text_lower.count(query_lower)
                # 개별 단어 매칭
                query_words = query_lower.split()
                for word in query_words:
                    if len(word) > 2 and word in text_lower:
                        score += 1
        
        return score

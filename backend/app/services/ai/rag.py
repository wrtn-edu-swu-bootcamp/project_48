"""
RAG (Retrieval-Augmented Generation) 파이프라인
"""
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from app.services.search import SearchService
from app.services.ai.client import get_gemini_client
from app.services.ai.prompts import SYSTEM_PROMPT, create_rag_prompt
from app.services.classifier import QuestionClassifier
from app.models.question_log import QuestionCategory
import logging

logger = logging.getLogger(__name__)


class RAGPipeline:
    """RAG 파이프라인 클래스"""
    
    def __init__(self, db: Session):
        """
        RAG 파이프라인 초기화
        
        Args:
            db: 데이터베이스 세션
        """
        self.db = db
        self.search_service = SearchService(db)
        self.gemini_client = get_gemini_client()
        self.classifier = QuestionClassifier()
    
    async def process_question(
        self,
        question: str,
        use_hybrid_search: bool = True,
    ) -> Dict[str, Any]:
        """
        질문 처리 (전체 RAG 파이프라인)
        
        Args:
            question: 사용자 질문
            use_hybrid_search: 하이브리드 검색 사용 여부
            
        Returns:
            답변 및 메타데이터
        """
        try:
            logger.info(f"질문 처리 시작: {question}")
            
            # 1. 질문 분류
            category = self.classifier.classify(question)
            logger.info(f"질문 카테고리: {category}")
            
            # 2. 관련 정보 검색
            if use_hybrid_search:
                search_results = self.search_service.hybrid_search(
                    query=question,
                    category=category,
                    limit=5
                )
            else:
                search_results = self.search_service.search_by_vector(
                    query=question,
                    category=category,
                    limit=5
                )
            
            logger.info(f"검색 결과 수: {len(search_results)}")
            
            # 3. 검색 결과 없을 때 폴백
            if not search_results:
                return self._create_fallback_response(question, category)
            
            # 4. RAG 프롬프트 생성
            rag_prompt = create_rag_prompt(question, search_results)
            
            # 5. Gemini API를 사용하여 답변 생성
            answer = await self.gemini_client.generate_response(
                user_message=rag_prompt,
                system_prompt=SYSTEM_PROMPT,
                max_tokens=2000
            )
            
            # 6. 출처 정보 추출
            sources = self._extract_sources(search_results)
            
            # 7. 응답 구조화
            response = {
                "answer": answer,
                "sources": sources,
                "category": category.value if isinstance(category, QuestionCategory) else category,
                "search_results_count": len(search_results),
                "success": True
            }
            
            logger.info("질문 처리 완료")
            return response
            
        except Exception as e:
            logger.error(f"RAG 파이프라인 오류: {e}")
            return self._create_error_response(str(e))
    
    def _extract_sources(self, search_results: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """
        검색 결과에서 출처 정보 추출
        
        Args:
            search_results: 검색 결과 리스트
            
        Returns:
            출처 정보 리스트
        """
        sources = []
        seen_sources = set()
        
        for result in search_results:
            source = result.get('source', '알 수 없음')
            if source not in seen_sources:
                sources.append({
                    "name": source,
                    "url": None,  # 향후 확장: 실제 URL 추가
                })
                seen_sources.add(source)
        
        return sources
    
    def _create_fallback_response(
        self,
        question: str,
        category: QuestionCategory
    ) -> Dict[str, Any]:
        """
        폴백 응답 생성 (검색 결과 없을 때)
        
        Args:
            question: 사용자 질문
            category: 질문 카테고리
            
        Returns:
            폴백 응답
        """
        fallback_answer = f"""죄송해요. "{question}"에 대한 정보를 현재 제공된 데이터에서 찾을 수 없어요.

**추천 방법:**
- 학교 행정실에 직접 문의해보세요
- 학과 사무실에 문의해보세요
- 학생성장지원시스템을 확인해보세요
- 아래 '상담원 연결' 버튼을 클릭해서 인간 상담원과 연결하세요

다른 궁금하신 점이 있으신가요?"""
        
        return {
            "answer": fallback_answer,
            "sources": [],
            "category": category.value if isinstance(category, QuestionCategory) else category,
            "search_results_count": 0,
            "success": True,
            "is_fallback": True
        }
    
    def _create_error_response(self, error_message: str) -> Dict[str, Any]:
        """
        에러 응답 생성
        
        Args:
            error_message: 에러 메시지
            
        Returns:
            에러 응답
        """
        return {
            "answer": "죄송해요. 일시적인 오류가 발생했어요. 잠시 후 다시 시도해주세요.",
            "sources": [],
            "category": "error",
            "search_results_count": 0,
            "success": False,
            "error": error_message
        }


def get_rag_pipeline(db: Session) -> RAGPipeline:
    """RAG 파이프라인 인스턴스 생성"""
    return RAGPipeline(db)

"""
챗봇 API 엔드포인트
"""
import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.ai.rag import get_rag_pipeline
from app.services.ai.fallback import get_fallback_handler
from app.models.question_log import QuestionLog, QuestionStatus, QuestionCategory
from datetime import datetime

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/api/v1/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
):
    """
    챗봇 질문 처리 엔드포인트
    
    사용자의 질문을 받아서 분류하고, 관련 정보를 검색한 후 답변을 생성합니다.
    
    **처리 흐름:**
    1. 질문 받기
    2. 질문 분류 (학사일정, 공지사항, 지원프로그램, 학사용어)
    3. 벡터 검색 + 키워드 검색 (하이브리드)
    4. Claude API를 사용하여 답변 생성
    5. 답변 구조화 및 출처 표기
    6. 질문 로그 저장
    """
    try:
        logger.info(f"채팅 요청 받음: {request.question}")
        
        # RAG 파이프라인을 사용하여 답변 생성
        rag_pipeline = get_rag_pipeline(db)
        rag_result = await rag_pipeline.process_question(request.question)

        # 응답 구성
        response = ChatResponse(
            answer=rag_result["answer"],
            category=rag_result.get("category", "기타"),
            sources=rag_result.get("sources", []),
        )
        
        # 질문 로그 저장
        try:
            # 카테고리 파싱
            category_map = {
                "학사일정": QuestionCategory.ACADEMIC_SCHEDULE,
                "공지사항": QuestionCategory.NOTICE,
                "지원프로그램": QuestionCategory.SUPPORT_PROGRAM,
                "학사정보": QuestionCategory.ACADEMIC_INFO,
            }
            category_enum = category_map.get(
                rag_result.get("category", "기타"),
                QuestionCategory.OTHER
            )
            
            question_log = QuestionLog(
                question=request.question,
                answer=response.answer,
                category=category_enum,
                status=QuestionStatus.COMPLETED if rag_result.get("success") else QuestionStatus.FAILED,
                created_at=datetime.now(),
            )
            db.add(question_log)
            db.commit()
            logger.info(f"질문 로그 저장 완료: ID={question_log.id}")
        except Exception as log_error:
            logger.error(f"질문 로그 저장 실패: {log_error}")
            # 로그 저장 실패해도 응답은 반환
        
        return response
        
    except Exception as e:
        # 에러 발생 시 폴백 답변 사용
        logger.error(f"채팅 API 에러: {str(e)}", exc_info=True)

        fallback_handler = get_fallback_handler()
        fallback_result = fallback_handler.get_error_response(str(e))

        response = ChatResponse(
            answer=fallback_result["answer"],
            category=fallback_result.get("category", "error"),
            sources=[],
        )

        # 에러 로그 저장
        try:
            question_log = QuestionLog(
                question=request.question,
                answer=response.answer,
                category=QuestionCategory.OTHER,
                status=QuestionStatus.FAILED,
                created_at=datetime.now(),
            )
            db.add(question_log)
            db.commit()
        except:
            pass  # 로그 저장도 실패하면 무시

        # 에러가 발생했어도 폴백 답변은 반환
        return response

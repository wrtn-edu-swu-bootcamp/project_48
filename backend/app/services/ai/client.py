"""
Google Gemini API 클라이언트
"""
import google.generativeai as genai
from app.core.config import settings
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)


class GeminiClient:
    """Gemini API 클라이언트 클래스"""
    
    def __init__(self):
        """Gemini 클라이언트 초기화"""
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model_name = "gemini-2.0-flash-exp"  # 최신 Gemini 2.0 Flash 모델
        self.model = genai.GenerativeModel(
            model_name=self.model_name,
            generation_config={
                "temperature": 0.7,  # 답변 다양성 확보
                "top_p": 0.95,
                "top_k": 40,
                "max_output_tokens": 2048,
            }
        )
        logger.info("✓ Gemini 클라이언트 초기화 완료")
    
    async def generate_response(
        self,
        user_message: str,
        system_prompt: str,
        context: Optional[List[Dict[str, str]]] = None,
        max_tokens: int = 2000,
    ) -> str:
        """
        Gemini API를 사용하여 응답 생성
        
        Args:
            user_message: 사용자 메시지
            system_prompt: 시스템 프롬프트
            context: 검색된 컨텍스트 (선택)
            max_tokens: 최대 토큰 수
            
        Returns:
            생성된 응답
        """
        try:
            # 컨텍스트가 있으면 메시지에 포함
            if context:
                context_text = self._format_context(context)
                full_message = f"{context_text}\n\n질문: {user_message}"
            else:
                full_message = user_message
            
            # 시스템 프롬프트와 사용자 메시지를 결합
            # Gemini는 시스템 프롬프트를 별도로 받지 않으므로 메시지 앞에 추가
            combined_prompt = f"{system_prompt}\n\n{full_message}"
            
            # Gemini API 호출
            response = self.model.generate_content(
                combined_prompt,
                generation_config=genai.GenerationConfig(
                    max_output_tokens=max_tokens,
                    temperature=0.7,
                )
            )
            
            # 응답 추출
            if response.candidates and len(response.candidates) > 0:
                answer = response.candidates[0].content.parts[0].text
            else:
                raise Exception("Gemini API가 유효한 응답을 생성하지 못했습니다.")
            
            logger.info(f"Gemini API 호출 성공")
            
            return answer
            
        except Exception as e:
            logger.error(f"Gemini API 호출 중 오류: {e}")
            raise
    
    def _format_context(self, context: List[Dict[str, str]]) -> str:
        """
        컨텍스트를 포맷팅
        
        Args:
            context: 컨텍스트 리스트
            
        Returns:
            포맷팅된 컨텍스트 문자열
        """
        formatted = "다음은 참고할 정보입니다:\n\n"
        
        for idx, item in enumerate(context, 1):
            formatted += f"[문서 {idx}]\n"
            formatted += f"출처: {item.get('source', '알 수 없음')}\n"
            
            if 'title' in item:
                formatted += f"제목: {item['title']}\n"
            if 'name' in item:
                formatted += f"이름: {item['name']}\n"
            if 'term' in item:
                formatted += f"용어: {item['term']}\n"
            
            if 'content' in item:
                formatted += f"내용: {item['content']}\n"
            elif 'description' in item:
                formatted += f"설명: {item['description']}\n"
            elif 'definition' in item:
                formatted += f"정의: {item['definition']}\n"
            
            formatted += "\n"
        
        return formatted


# 싱글톤 인스턴스
_gemini_client = None


def get_gemini_client() -> GeminiClient:
    """Gemini 클라이언트 인스턴스 반환 (싱글톤)"""
    global _gemini_client
    if _gemini_client is None:
        _gemini_client = GeminiClient()
    return _gemini_client

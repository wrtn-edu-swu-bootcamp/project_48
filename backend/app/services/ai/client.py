"""
Anthropic Claude API 클라이언트
"""
import anthropic
from app.core.config import settings
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)


class ClaudeClient:
    """Claude API 클라이언트 클래스"""
    
    def __init__(self):
        """Claude 클라이언트 초기화"""
        self.client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        self.model = "claude-3-5-sonnet-20241022"  # 최신 Claude 모델
        logger.info("✓ Claude 클라이언트 초기화 완료")
    
    async def generate_response(
        self,
        user_message: str,
        system_prompt: str,
        context: Optional[List[Dict[str, str]]] = None,
        max_tokens: int = 2000,
    ) -> str:
        """
        Claude API를 사용하여 응답 생성
        
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
            
            # Claude API 호출
            message = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": full_message}
                ]
            )
            
            # 응답 추출
            response = message.content[0].text
            
            logger.info(f"Claude API 호출 성공 (토큰: {message.usage.input_tokens + message.usage.output_tokens})")
            
            return response
            
        except Exception as e:
            logger.error(f"Claude API 호출 중 오류: {e}")
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
_claude_client = None


def get_claude_client() -> ClaudeClient:
    """Claude 클라이언트 인스턴스 반환 (싱글톤)"""
    global _claude_client
    if _claude_client is None:
        _claude_client = ClaudeClient()
    return _claude_client

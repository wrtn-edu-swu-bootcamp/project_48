import { useState } from 'react';
import { sendChatMessage } from '../utils/api';

/**
 * useChat 훅
 * 챗봇 메시지 관리 및 API 연동 로직
 * 추후 실제 API와 연동할 수 있도록 구조 설계
 */
export function useChat() {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  /**
   * 메시지 전송 함수
   * @param {string} text - 사용자가 입력한 메시지
   */
  const sendMessage = async (text) => {
    if (!text.trim()) return;

    // 사용자 메시지 추가
    const userMessage = {
      type: 'user',
      text: text,
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, userMessage]);
    setLoading(true);

    try {
      // API 호출 (현재는 모의 응답)
      const response = await sendChatMessage(text);
      
      // 봇 응답 추가
      const botMessage = {
        type: 'bot',
        text: response.text,
        source: response.source,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      // 에러 처리
      const errorMessage = {
        type: 'bot',
        text: '죄송해요. 일시적인 오류가 발생했어요. 잠시 후 다시 시도해주세요.',
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  return { messages, sendMessage, loading };
}

import React, { useState, useRef, useEffect } from 'react';
import SendButton from './SendButton';

/**
 * InputArea 컴포넌트
 * 질문 입력창과 전송 버튼이 있는 하단 입력 영역
 */
function InputArea({ onSendMessage, loading }) {
  const [input, setInput] = useState('');
  const inputRef = useRef(null);

  // Enter 키로 전송 (Shift+Enter는 줄바꿈)
  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleSend = () => {
    if (input.trim() && !loading) {
      onSendMessage(input.trim());
      setInput('');
      inputRef.current?.focus();
    }
  };

  // 컴포넌트 마운트 시 입력창에 포커스
  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  return (
    <div className="fixed bottom-0 left-0 right-0 z-50 bg-white border-t border-gray-200 shadow-lg">
      <div className="max-w-3xl mx-auto px-4 py-3">
        <div className="flex items-center space-x-2">
          {/* 입력창 */}
          <input
            ref={inputRef}
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="궁금한 것을 물어보세요 (예: 수강신청 일정, 장학금 신청 등)"
            disabled={loading}
            className="flex-1 px-4 py-3 text-base border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-burgundy focus:border-transparent disabled:bg-gray-100 disabled:cursor-not-allowed"
            aria-label="질문 입력"
          />
          
          {/* 전송 버튼 */}
          <SendButton 
            onClick={handleSend} 
            disabled={!input.trim() || loading}
          />
        </div>
      </div>
    </div>
  );
}

export default InputArea;

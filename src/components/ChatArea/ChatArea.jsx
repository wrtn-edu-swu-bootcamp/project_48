import React, { useEffect, useRef } from 'react';
import MessageList from './MessageList';
import QuestionExamples from './QuestionExamples';

/**
 * ChatArea 컴포넌트
 * 챗봇 대화 영역과 질문 예시를 표시하는 메인 콘텐츠 영역
 */
function ChatArea({ messages, loading, onQuestionClick }) {
  const chatEndRef = useRef(null);

  // 메시지가 추가될 때마다 스크롤을 하단으로 이동
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  return (
    <div className="w-full">
      {/* 질문 예시 버튼 - 메시지가 없을 때만 표시 */}
      {messages.length === 0 && (
        <QuestionExamples onQuestionClick={onQuestionClick} />
      )}
      
      {/* 메시지 리스트 */}
      <MessageList messages={messages} loading={loading} />
      
      {/* 스크롤 위치 조정용 요소 */}
      <div ref={chatEndRef} />
    </div>
  );
}

export default ChatArea;

import React from 'react';
import UserMessage from './UserMessage';
import BotMessage from './BotMessage';

/**
 * MessageList 컴포넌트
 * 사용자와 봇의 메시지를 리스트로 표시
 */
function MessageList({ messages, loading }) {
  return (
    <div className="space-y-3 mt-6">
      {messages.map((message, index) => (
        <div key={index}>
          {message.type === 'user' ? (
            <UserMessage text={message.text} />
          ) : (
            <BotMessage 
              text={message.text} 
              source={message.source}
            />
          )}
        </div>
      ))}
      
      {/* 로딩 인디케이터 */}
      {loading && (
        <div className="flex items-start space-x-2">
          <div className="bg-gray-100 rounded-2xl px-4 py-3 max-w-[80%]">
            <div className="flex space-x-1">
              <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
              <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
              <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default MessageList;

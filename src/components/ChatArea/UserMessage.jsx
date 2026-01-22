import React from 'react';

/**
 * UserMessage 컴포넌트
 * 사용자 메시지를 우측 정렬로 표시
 */
function UserMessage({ text }) {
  return (
    <div className="flex justify-end">
      <div className="bg-burgundy text-white rounded-2xl px-4 py-3 max-w-[80%] shadow-sm">
        <p className="text-base leading-relaxed whitespace-pre-wrap">{text}</p>
      </div>
    </div>
  );
}

export default UserMessage;

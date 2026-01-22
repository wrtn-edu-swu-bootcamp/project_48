import React from 'react';

/**
 * BotMessage 컴포넌트
 * 봇 메시지를 좌측 정렬로 표시, 출처 표기 포함
 */
function BotMessage({ text, source }) {
  return (
    <div className="flex justify-start">
      <div className="bg-gray-100 text-gray-900 rounded-2xl px-4 py-3 max-w-[80%] shadow-sm">
        <p className="text-base leading-relaxed whitespace-pre-wrap">{text}</p>
        {source && (
          <p className="text-xs text-gray-500 mt-2 pt-2 border-t border-gray-200">
            출처: {source}
          </p>
        )}
      </div>
    </div>
  );
}

export default BotMessage;

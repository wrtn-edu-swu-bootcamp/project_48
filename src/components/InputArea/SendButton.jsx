import React from 'react';

/**
 * SendButton 컴포넌트
 * 메시지 전송 버튼
 */
function SendButton({ onClick, disabled }) {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className="bg-burgundy text-white rounded-lg px-5 py-3 min-w-[44px] min-h-[44px] flex items-center justify-center hover:bg-opacity-90 transition-colors duration-150 focus:outline-none focus:ring-2 focus:ring-burgundy focus:ring-offset-2 disabled:bg-gray-300 disabled:cursor-not-allowed"
      aria-label="메시지 전송"
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        className="h-5 w-5"
        viewBox="0 0 20 20"
        fill="currentColor"
      >
        <path d="M10.894 2.553a1 1 0 00-1.788 0l-7 14a1 1 0 001.169 1.409l5-1.429A1 1 0 009 15.571V11a1 1 0 112 0v4.571a1 1 0 00.725.962l5 1.428a1 1 0 001.17-1.408l-7-14z" />
      </svg>
    </button>
  );
}

export default SendButton;

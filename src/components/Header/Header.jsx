import React from 'react';

/**
 * Header 컴포넌트
 * 서비스명과 간단한 설명을 표시하는 상단 헤더
 */
function Header() {
  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-white shadow-sm border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 py-4 md:py-5">
        <h1 className="text-xl md:text-2xl font-bold text-gray-900 mb-1">
          AI 신입생 도우미
        </h1>
        <p className="text-sm md:text-base text-gray-600 leading-relaxed">
          궁금한 학사 정보를 쉽고 빠르게 물어보세요
        </p>
      </div>
    </header>
  );
}

export default Header;

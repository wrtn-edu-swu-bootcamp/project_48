import React from 'react';

/**
 * Footer 컴포넌트
 * 자주 묻는 질문, 학사 일정, 지원 프로그램 링크를 제공하는 하단 영역
 */
function Footer() {
  const footerLinks = [
    { label: '자주 묻는 질문', href: '#faq' },
    { label: '학사 일정 보기', href: '#schedule' },
    { label: '지원 프로그램 안내', href: '#programs' },
  ];

  return (
    <footer className="bg-gray-50 border-t border-gray-200 py-4 mt-auto">
      <div className="max-w-7xl mx-auto px-4">
        <div className="flex flex-col md:flex-row justify-center items-center space-y-2 md:space-y-0 md:space-x-6">
          {footerLinks.map((link, index) => (
            <a
              key={index}
              href={link.href}
              className="text-sm text-burgundy hover:underline focus:outline-none focus:ring-2 focus:ring-burgundy focus:ring-offset-2 rounded px-2 py-1"
              aria-label={link.label}
            >
              {link.label}
            </a>
          ))}
        </div>
        <p className="text-xs text-gray-500 text-center mt-3">
          서울여자대학교 AI 신입생 도우미
        </p>
      </div>
    </footer>
  );
}

export default Footer;

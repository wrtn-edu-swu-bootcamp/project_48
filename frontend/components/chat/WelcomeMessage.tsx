"use client";

import React from "react";

export const WelcomeMessage: React.FC = () => {
  return (
    <div className="flex items-start space-x-3">
      <div className="w-10 h-10 rounded-full bg-[var(--color-primary)] flex items-center justify-center flex-shrink-0">
        <span className="text-white text-sm font-bold">AI</span>
      </div>
      <div className="flex-1">
        <div className="bg-[var(--color-background-tertiary)] rounded-2xl rounded-tl-sm px-5 py-4">
          <p className="text-base text-[var(--color-text-primary)] leading-relaxed">
            안녕하세요! 저는 AI 신입생 도우미입니다. 학사 일정, 공지사항, 지원
            프로그램에 대해 도와드릴 수 있어요. 궁금한 점을 자유롭게 물어보세요.
          </p>
        </div>
        <p className="text-xs text-[var(--color-text-tertiary)] mt-1 px-1 italic">
          출처: AI 신입생 도우미
        </p>
      </div>
    </div>
  );
};

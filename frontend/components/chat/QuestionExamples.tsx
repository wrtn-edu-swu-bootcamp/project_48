"use client";

import React from "react";
import { useRouter } from "next/navigation";

export const ExampleQuestions: React.FC = () => {
  const router = useRouter();

  const exampleQuestions = [
    "수강신청은 언제 하나요?",
    "장학금 신청 방법이 궁금해요",
    "학사 용어가 어려워요",
  ];

  const handleQuestionClick = (question: string) => {
    router.push(`/chat?q=${encodeURIComponent(question)}`);
  };

  return (
    <div className="space-y-3 pt-4">
      <p className="text-sm font-medium text-[var(--color-text-secondary)] px-1">
        이런 질문을 해보세요
      </p>
      <div className="flex flex-wrap gap-2">
        {exampleQuestions.map((question, index) => (
          <button
            key={index}
            onClick={() => handleQuestionClick(question)}
            className="inline-flex items-center px-4 py-2 rounded-full border border-[var(--color-primary)] bg-[var(--color-background)] text-[var(--color-primary)] text-sm hover:bg-[var(--color-primary)] hover:text-[var(--color-text-on-primary)] transition-colors focus:outline-none focus:ring-2 focus:ring-[var(--color-primary)] focus:ring-offset-2"
          >
            {question}
          </button>
        ))}
      </div>
    </div>
  );
};

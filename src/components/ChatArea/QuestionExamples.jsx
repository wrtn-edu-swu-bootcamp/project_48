import React from 'react';

/**
 * QuestionExamples 컴포넌트
 * 첫 방문자를 위한 질문 예시 버튼들
 */
function QuestionExamples({ onQuestionClick }) {
  const exampleQuestions = [
    "수강신청은 언제 하나요?",
    "장학금 신청 방법이 궁금해요",
    "학사 용어가 어려워요"
  ];

  return (
    <div className="space-y-3">
      {/* 환영 메시지 */}
      <div className="flex justify-start mb-6">
        <div className="bg-gray-100 text-gray-900 rounded-2xl px-4 py-3 max-w-[80%]">
          <p className="text-base leading-relaxed">
            안녕하세요! AI 신입생 도우미입니다. 😊<br />
            궁금한 학사 정보를 물어보시거나 아래 예시 질문을 클릭해보세요.
          </p>
        </div>
      </div>

      {/* 질문 예시 버튼 */}
      <div className="flex flex-col space-y-2">
        {exampleQuestions.map((question, index) => (
          <button
            key={index}
            onClick={() => onQuestionClick(question)}
            className="w-full text-left bg-white border-2 border-burgundy text-burgundy rounded-lg px-4 py-3 hover:bg-gray-50 transition-colors duration-150 focus:outline-none focus:ring-2 focus:ring-burgundy focus:ring-offset-2"
            aria-label={`질문 예시: ${question}`}
          >
            <span className="text-sm md:text-base">{question}</span>
          </button>
        ))}
      </div>
    </div>
  );
}

export default QuestionExamples;

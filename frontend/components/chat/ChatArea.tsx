"use client";

import React, { useEffect, useRef } from "react";
import { MessageList } from "./MessageList";
import { WelcomeMessage } from "./WelcomeMessage";
import { ExampleQuestions } from "./QuestionExamples";

export interface Message {
  id: string;
  role: "user" | "bot";
  content: string;
  timestamp: Date;
  source?: string;
}

export interface ChatAreaProps {
  messages: Message[];
  isLoading?: boolean;
}

export const ChatArea: React.FC<ChatAreaProps> = ({ messages, isLoading }) => {
  const chatEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // 새 메시지가 추가되면 스크롤
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading]);

  return (
    <div className="h-full overflow-y-auto px-4 py-6 space-y-4">
      {messages.length === 0 ? (
        <>
          <WelcomeMessage />
          <ExampleQuestions />
        </>
      ) : (
        <>
          <MessageList messages={messages} />
          {isLoading && (
            <div className="flex items-start space-x-3">
              <div className="w-8 h-8 rounded-full bg-[var(--color-primary)] flex items-center justify-center flex-shrink-0">
                <span className="text-white text-sm font-bold">AI</span>
              </div>
              <div className="flex-1">
                <div className="bg-[var(--color-background-tertiary)] rounded-lg px-4 py-3 inline-block">
                  <div className="flex space-x-1">
                    <div className="w-2 h-2 bg-[var(--color-text-secondary)] rounded-full animate-bounce" style={{ animationDelay: "0ms" }} />
                    <div className="w-2 h-2 bg-[var(--color-text-secondary)] rounded-full animate-bounce" style={{ animationDelay: "150ms" }} />
                    <div className="w-2 h-2 bg-[var(--color-text-secondary)] rounded-full animate-bounce" style={{ animationDelay: "300ms" }} />
                  </div>
                </div>
              </div>
            </div>
          )}
        </>
      )}
      <div ref={chatEndRef} />
    </div>
  );
};

"use client";

import React, { useState, useRef, useEffect } from "react";
import { PaperAirplaneIcon } from "@heroicons/react/24/outline";

export interface InputAreaProps {
  onSendMessage: (message: string) => void;
  isLoading?: boolean;
}

export const InputArea: React.FC<InputAreaProps> = ({
  onSendMessage,
  isLoading,
}) => {
  const [message, setMessage] = useState("");
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (message.trim() && !isLoading) {
      onSendMessage(message.trim());
      setMessage("");
      if (textareaRef.current) {
        textareaRef.current.style.height = "auto";
      }
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`;
    }
  }, [message]);

  return (
    <form onSubmit={handleSubmit} className="flex items-end space-x-3">
      <div className="flex-1">
        <textarea
          ref={textareaRef}
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="궁금한 것을 물어보세요 (예: 수강신청 일정, 장학금 신청 등)"
          rows={1}
          className="w-full min-h-[44px] max-h-[120px] px-4 py-3 rounded-2xl border border-[var(--color-border-primary)] bg-[var(--color-background)] text-[var(--color-text-primary)] placeholder:text-[var(--color-text-placeholder)] focus:outline-none focus:ring-2 focus:ring-[var(--color-primary)] focus:border-transparent resize-none overflow-y-auto"
          disabled={isLoading}
          aria-label="질문 입력"
        />
        <p className="text-xs text-[var(--color-text-tertiary)] mt-1 px-1">
          Enter로 전송, Shift+Enter로 줄바꿈
        </p>
      </div>
      <button
        type="submit"
        disabled={!message.trim() || isLoading}
        className="w-11 h-11 rounded-full bg-[var(--color-primary)] text-[var(--color-text-on-primary)] flex items-center justify-center hover:bg-[var(--color-primary-hover)] transition-colors disabled:opacity-50 disabled:cursor-not-allowed focus:outline-none focus:ring-2 focus:ring-[var(--color-primary)] focus:ring-offset-2"
        aria-label="전송"
      >
        <PaperAirplaneIcon className="w-5 h-5" />
      </button>
    </form>
  );
};

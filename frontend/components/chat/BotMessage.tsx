"use client";

import React from "react";
import type { Message } from "./ChatArea";
import { FeedbackButtons } from "./FeedbackButtons";

export interface BotMessageProps {
  message: Message;
}

export const BotMessage: React.FC<BotMessageProps> = ({ message }) => {
  const formatTime = (date: Date) => {
    return new Intl.DateTimeFormat("ko-KR", {
      hour: "2-digit",
      minute: "2-digit",
    }).format(date);
  };

  return (
    <div className="flex items-start space-x-3">
      <div className="w-8 h-8 rounded-full bg-[var(--color-primary)] flex items-center justify-center flex-shrink-0">
        <span className="text-white text-sm font-bold">AI</span>
      </div>
      <div className="flex-1 max-w-[75%] md:max-w-[75%]">
        <div className="bg-[var(--color-background-tertiary)] rounded-2xl rounded-tl-sm px-4 py-3">
          <div className="text-base text-[var(--color-text-primary)] whitespace-pre-wrap break-words">
            {message.content}
          </div>
        </div>
        {message.source && (
          <p className="text-xs text-[var(--color-text-tertiary)] mt-1 px-1 italic">
            출처: {message.source}
          </p>
        )}
        <FeedbackButtons messageId={message.id} />
        <p className="text-xs text-[var(--color-text-tertiary)] mt-1 px-1">
          {formatTime(message.timestamp)}
        </p>
      </div>
    </div>
  );
};

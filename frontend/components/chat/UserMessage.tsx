"use client";

import React from "react";
import type { Message } from "./ChatArea";

export interface UserMessageProps {
  message: Message;
}

export const UserMessage: React.FC<UserMessageProps> = ({ message }) => {
  const formatTime = (date: Date) => {
    return new Intl.DateTimeFormat("ko-KR", {
      hour: "2-digit",
      minute: "2-digit",
    }).format(date);
  };

  return (
    <div className="flex justify-end">
      <div className="max-w-[75%] md:max-w-[75%]">
        <div className="bg-[var(--color-primary)] text-[var(--color-text-on-primary)] rounded-2xl rounded-tr-sm px-4 py-3">
          <p className="text-base whitespace-pre-wrap break-words">
            {message.content}
          </p>
        </div>
        <p className="text-xs text-[var(--color-text-tertiary)] mt-1 text-right px-1">
          {formatTime(message.timestamp)}
        </p>
      </div>
    </div>
  );
};

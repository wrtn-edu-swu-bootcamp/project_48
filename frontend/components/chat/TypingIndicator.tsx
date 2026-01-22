"use client";

import React from "react";

export const TypingIndicator: React.FC = () => {
  return (
    <div className="flex items-start space-x-3">
      <div className="w-8 h-8 rounded-full bg-[var(--color-primary)] flex items-center justify-center flex-shrink-0">
        <span className="text-white text-sm font-bold">AI</span>
      </div>
      <div className="flex-1">
        <div className="bg-[var(--color-background-tertiary)] rounded-lg px-4 py-3 inline-block">
          <div className="flex space-x-1">
            <div
              className="w-2 h-2 bg-[var(--color-text-secondary)] rounded-full animate-bounce"
              style={{ animationDelay: "0ms" }}
            />
            <div
              className="w-2 h-2 bg-[var(--color-text-secondary)] rounded-full animate-bounce"
              style={{ animationDelay: "150ms" }}
            />
            <div
              className="w-2 h-2 bg-[var(--color-text-secondary)] rounded-full animate-bounce"
              style={{ animationDelay: "300ms" }}
            />
          </div>
        </div>
      </div>
    </div>
  );
};

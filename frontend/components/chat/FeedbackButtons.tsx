"use client";

import React, { useState } from "react";
import { HandThumbUpIcon, HandThumbDownIcon } from "@heroicons/react/24/outline";
import { HandThumbUpIcon as HandThumbUpIconSolid } from "@heroicons/react/24/solid";

export interface FeedbackButtonsProps {
  messageId: string;
  onFeedback?: (messageId: string, feedback: "positive" | "negative") => void;
}

export const FeedbackButtons: React.FC<FeedbackButtonsProps> = ({
  messageId,
  onFeedback,
}) => {
  const [feedback, setFeedback] = useState<"positive" | "negative" | null>(
    null
  );

  const handleFeedback = (type: "positive" | "negative") => {
    setFeedback(type);
    onFeedback?.(messageId, type);
  };

  return (
    <div className="flex items-center space-x-4 mt-2 px-1">
      <span className="text-xs text-[var(--color-text-secondary)]">
        도움이 되었나요?
      </span>
      <button
        onClick={() => handleFeedback("positive")}
        className={`p-1 rounded transition-colors ${
          feedback === "positive"
            ? "text-[var(--color-primary)]"
            : "text-[var(--color-text-tertiary)] hover:text-[var(--color-primary)]"
        }`}
        aria-label="좋아요"
      >
        {feedback === "positive" ? (
          <HandThumbUpIconSolid className="w-5 h-5" />
        ) : (
          <HandThumbUpIcon className="w-5 h-5" />
        )}
      </button>
      <button
        onClick={() => handleFeedback("negative")}
        className={`p-1 rounded transition-colors ${
          feedback === "negative"
            ? "text-[var(--color-error)]"
            : "text-[var(--color-text-tertiary)] hover:text-[var(--color-error)]"
        }`}
        aria-label="싫어요"
      >
        {feedback === "negative" ? (
          <HandThumbDownIcon className="w-5 h-5 fill-current" />
        ) : (
          <HandThumbDownIcon className="w-5 h-5" />
        )}
      </button>
    </div>
  );
};

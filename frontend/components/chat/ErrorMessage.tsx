"use client";

import React from "react";
import { ExclamationTriangleIcon } from "@heroicons/react/24/outline";
import { Button } from "@/components/ui/Button";

export interface ErrorMessageProps {
  message?: string;
  onRetry?: () => void;
}

export const ErrorMessage: React.FC<ErrorMessageProps> = ({
  message = "일시적인 오류가 발생했어요. 잠시 후 다시 시도해주세요.",
  onRetry,
}) => {
  return (
    <div className="flex items-start space-x-3">
      <div className="w-8 h-8 rounded-full bg-[var(--color-error)] flex items-center justify-center flex-shrink-0">
        <ExclamationTriangleIcon className="w-5 h-5 text-white" />
      </div>
      <div className="flex-1">
        <div className="bg-[var(--color-error-bg)] border-l-4 border-[var(--color-error)] rounded-lg px-4 py-3">
          <p className="text-sm text-[var(--color-text-primary)]">{message}</p>
          {onRetry && (
            <div className="mt-3">
              <Button size="small" variant="secondary" onClick={onRetry}>
                다시 시도
              </Button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

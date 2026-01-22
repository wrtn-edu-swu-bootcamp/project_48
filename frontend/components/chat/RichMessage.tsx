"use client";

import React from "react";
import { Card } from "@/components/ui/Card";

export interface RichMessageProps {
  type: "card" | "list";
  items: Array<{
    title: string;
    description?: string;
    action?: {
      label: string;
      onClick: () => void;
    };
  }>;
}

export const RichMessage: React.FC<RichMessageProps> = ({ type, items }) => {
  if (type === "card") {
    return (
      <div className="space-y-3">
        {items.map((item, index) => (
          <Card key={index} hover={!!item.action} clickable={!!item.action}>
            <div className="space-y-2">
              <h4 className="text-base font-bold text-[var(--color-text-primary)]">
                {item.title}
              </h4>
              {item.description && (
                <p className="text-sm text-[var(--color-text-secondary)]">
                  {item.description}
                </p>
              )}
              {item.action && (
                <button
                  onClick={item.action.onClick}
                  className="text-sm text-[var(--color-primary)] hover:underline"
                >
                  {item.action.label}
                </button>
              )}
            </div>
          </Card>
        ))}
      </div>
    );
  }

  if (type === "list") {
    return (
      <ul className="space-y-2 list-disc list-inside">
        {items.map((item, index) => (
          <li key={index} className="text-base text-[var(--color-text-primary)]">
            <span className="font-semibold">{item.title}</span>
            {item.description && (
              <span className="text-[var(--color-text-secondary)] ml-2">
                {item.description}
              </span>
            )}
          </li>
        ))}
      </ul>
    );
  }

  return null;
};

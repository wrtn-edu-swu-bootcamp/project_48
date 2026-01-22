"use client";

import React from "react";
import { cn } from "@/lib/utils";

export interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  variant?: "default" | "success" | "warning" | "error" | "info";
}

export const Badge = React.forwardRef<HTMLSpanElement, BadgeProps>(
  ({ className, variant = "default", children, ...props }, ref) => {
    const variants = {
      default:
        "bg-[var(--color-background-tertiary)] text-[var(--color-text-secondary)]",
      success:
        "bg-[var(--color-success-bg)] text-[var(--color-success)]",
      warning:
        "bg-[var(--color-warning-bg)] text-[var(--color-warning)]",
      error: "bg-[var(--color-error-bg)] text-[var(--color-error)]",
      info: "bg-[var(--color-info-bg)] text-[var(--color-info)]",
    };

    return (
      <span
        ref={ref}
        className={cn(
          "inline-flex items-center px-2 py-1 rounded-full text-xs font-medium",
          variants[variant],
          className
        )}
        {...props}
      >
        {children}
      </span>
    );
  }
);

Badge.displayName = "Badge";

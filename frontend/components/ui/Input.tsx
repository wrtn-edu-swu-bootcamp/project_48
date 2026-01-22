"use client";

import React from "react";
import { cn } from "@/lib/utils";

export interface InputProps
  extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  helperText?: string;
}

export const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className, label, error, helperText, id, ...props }, ref) => {
    const inputId = id || `input-${Math.random().toString(36).substr(2, 9)}`;

    return (
      <div className="w-full">
        {label && (
          <label
            htmlFor={inputId}
            className="block text-sm font-medium text-[var(--color-text-primary)] mb-2"
          >
            {label}
          </label>
        )}
        <input
          ref={ref}
          id={inputId}
          className={cn(
            "w-full h-11 px-4 py-2 text-base",
            "bg-[var(--color-background)]",
            "border border-[var(--color-border-primary)]",
            "rounded-lg",
            "text-[var(--color-text-primary)]",
            "placeholder:text-[var(--color-text-placeholder)]",
            "focus:outline-none focus:ring-2 focus:ring-[var(--color-primary)] focus:border-transparent",
            "disabled:opacity-50 disabled:cursor-not-allowed",
            error &&
              "border-[var(--color-error)] focus:ring-[var(--color-error)]",
            className
          )}
          aria-invalid={error ? "true" : "false"}
          aria-describedby={
            error || helperText
              ? `${inputId}-${error ? "error" : "helper"}`
              : undefined
          }
          {...props}
        />
        {error && (
          <p
            id={`${inputId}-error`}
            className="mt-1 text-sm text-[var(--color-error)]"
            role="alert"
          >
            {error}
          </p>
        )}
        {helperText && !error && (
          <p
            id={`${inputId}-helper`}
            className="mt-1 text-sm text-[var(--color-text-secondary)]"
          >
            {helperText}
          </p>
        )}
      </div>
    );
  }
);

Input.displayName = "Input";

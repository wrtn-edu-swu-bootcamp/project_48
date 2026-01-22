"use client";

import React from "react";
import { cn } from "@/lib/utils";

export interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  hover?: boolean;
  clickable?: boolean;
}

export const Card = React.forwardRef<HTMLDivElement, CardProps>(
  ({ className, hover = false, clickable = false, children, ...props }, ref) => {
    return (
      <div
        ref={ref}
        className={cn(
          "bg-[var(--color-background)]",
          "rounded-xl",
          "p-6",
          "border border-[var(--color-border-primary)]",
          "shadow-[var(--shadow-md)]",
          hover && "hover:shadow-[var(--shadow-lg)] hover:-translate-y-0.5 transition-all",
          clickable && "cursor-pointer",
          className
        )}
        {...props}
      >
        {children}
      </div>
    );
  }
);

Card.displayName = "Card";

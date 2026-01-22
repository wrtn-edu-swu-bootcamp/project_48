"use client";

import React from "react";
import Link from "next/link";
import { cn } from "@/lib/utils";

export interface HeaderProps {
  className?: string;
}

export const Header: React.FC<HeaderProps> = ({ className }) => {
  return (
    <header
      className={cn(
        "sticky top-0 z-50",
        "bg-[var(--color-background)]",
        "border-b border-[var(--color-border-primary)]",
        "h-20 md:h-24",
        className
      )}
    >
      <div className="max-w-7xl mx-auto px-4 md:px-6 h-full flex items-center">
        <Link href="/" className="flex items-center space-x-3">
          <h1 className="text-2xl md:text-3xl font-bold text-[var(--color-primary)]">
            AI 신입생 도우미
          </h1>
        </Link>
        <p className="hidden md:block ml-4 text-sm text-[var(--color-text-secondary)]">
          궁금한 학사 정보를 쉽고 빠르게 물어보세요
        </p>
      </div>
    </header>
  );
};

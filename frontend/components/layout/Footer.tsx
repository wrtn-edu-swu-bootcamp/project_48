"use client";

import React from "react";
import Link from "next/link";
import { cn } from "@/lib/utils";

export interface FooterProps {
  className?: string;
}

export const Footer: React.FC<FooterProps> = ({ className }) => {
  return (
    <footer
      className={cn(
        "bg-[var(--color-background-secondary)]",
        "border-t border-[var(--color-border-primary)]",
        "py-8 md:py-12",
        className
      )}
    >
      <div className="max-w-7xl mx-auto px-4 md:px-6">
        <div className="flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0">
          <div className="flex flex-wrap justify-center md:justify-start gap-4 md:gap-6">
            <Link
              href="/faq"
              className="text-sm text-[var(--color-text-secondary)] hover:text-[var(--color-primary)] transition-colors"
            >
              자주 묻는 질문
            </Link>
            <Link
              href="/schedules"
              className="text-sm text-[var(--color-text-secondary)] hover:text-[var(--color-primary)] transition-colors"
            >
              학사 일정 보기
            </Link>
            <Link
              href="/programs"
              className="text-sm text-[var(--color-text-secondary)] hover:text-[var(--color-primary)] transition-colors"
            >
              지원 프로그램 안내
            </Link>
            <Link
              href="/contact"
              className="text-sm text-[var(--color-text-secondary)] hover:text-[var(--color-primary)] transition-colors"
            >
              문의하기
            </Link>
          </div>
          <p className="text-xs text-[var(--color-text-tertiary)]">
            © 2025 서울여자대학교
          </p>
        </div>
      </div>
    </footer>
  );
};

"use client";

import React from "react";
import { Header } from "./Header";
import { Footer } from "./Footer";
import { cn } from "@/lib/utils";

export interface MainLayoutProps {
  children: React.ReactNode;
  className?: string;
}

export const MainLayout: React.FC<MainLayoutProps> = ({
  children,
  className,
}) => {
  return (
    <div className="min-h-screen flex flex-col">
      <Header />
      <main
        className={cn(
          "flex-1",
          "max-w-7xl mx-auto w-full px-4 md:px-6 py-8 md:py-12",
          className
        )}
      >
        {children}
      </main>
      <Footer />
    </div>
  );
};

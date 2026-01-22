"use client";

import React from "react";
import Link from "next/link";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import {
  CalendarIcon,
  BellIcon,
  LightBulbIcon,
  ArrowRightIcon,
} from "@heroicons/react/24/outline";

export default function HomePage() {
  const exampleQuestions = [
    "수강신청은 언제 하나요?",
    "장학금 신청 방법이 궁금해요",
    "학사 용어가 어려워요",
  ];

  const quickLinks = [
    {
      icon: CalendarIcon,
      title: "학사일정 보기",
      description: "수강신청, 등록금 납부 등 주요 일정 확인",
      href: "/schedules",
    },
    {
      icon: BellIcon,
      title: "공지사항 확인",
      description: "중요한 학교 공지 빠르게 확인",
      href: "/notices",
    },
    {
      icon: LightBulbIcon,
      title: "지원프로그램 안내",
      description: "장학금, 비교과 프로그램 등 안내",
      href: "/programs",
    },
  ];

  const serviceInfo = [
    {
      icon: "📅",
      title: "학사 일정 안내",
      description:
        "수강신청, 등록금 납부, 휴학 등 주요 일정을 한눈에 확인하세요",
    },
    {
      icon: "📢",
      title: "공지사항 안내",
      description:
        "중요한 학교 공지를 놓치지 않고 빠르게 확인하세요",
    },
    {
      icon: "💡",
      title: "지원 프로그램 안내",
      description:
        "장학금, 비교과, 멘토링 등 다양한 지원 프로그램을 알아보세요",
    },
  ];

  return (
    <div className="space-y-16 md:space-y-24">
      {/* Hero 섹션 */}
      <section className="text-center space-y-6 animate-fade-in">
        <h1 className="text-3xl md:text-4xl lg:text-5xl font-bold text-[var(--color-primary)]">
          안녕하세요! AI 신입생 도우미입니다
        </h1>
        <p className="text-lg md:text-xl text-[var(--color-text-secondary)] max-w-2xl mx-auto">
          학사 일정, 공지사항, 지원 프로그램을 한 번에 확인하세요
        </p>
        <div className="pt-4">
          <Link href="/chat">
            <Button size="large">지금 질문하기</Button>
          </Link>
        </div>
      </section>

      {/* Quick Links 섹션 */}
      <section className="space-y-6">
        <h2 className="text-2xl font-bold text-[var(--color-text-primary)]">
          빠른 안내
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 md:gap-6">
          {quickLinks.map((link) => {
            const Icon = link.icon;
            return (
              <Link key={link.href} href={link.href}>
                <Card hover clickable className="h-full">
                  <div className="flex flex-col items-center text-center space-y-4">
                    <div className="w-12 h-12 flex items-center justify-center rounded-full bg-[var(--color-primary)]/10">
                      <Icon className="w-8 h-8 text-[var(--color-primary)]" />
                    </div>
                    <div>
                      <h3 className="text-lg font-semibold text-[var(--color-text-primary)] mb-2">
                        {link.title}
                      </h3>
                      <p className="text-sm text-[var(--color-text-secondary)]">
                        {link.description}
                      </p>
                    </div>
                  </div>
                </Card>
              </Link>
            );
          })}
        </div>
      </section>

      {/* Example Questions 섹션 */}
      <section className="space-y-6">
        <h2 className="text-2xl font-bold text-[var(--color-text-primary)]">
          자주 묻는 질문
        </h2>
        <div className="space-y-3">
          {exampleQuestions.map((question, index) => (
            <Link key={index} href={`/chat?q=${encodeURIComponent(question)}`}>
              <Card
                hover
                clickable
                className="flex items-center justify-between group"
              >
                <span className="text-base text-[var(--color-text-primary)]">
                  {question}
                </span>
                <ArrowRightIcon className="w-5 h-5 text-[var(--color-primary)] opacity-0 group-hover:opacity-100 transition-opacity" />
              </Card>
            </Link>
          ))}
        </div>
      </section>

      {/* Service Info 섹션 */}
      <section className="space-y-6">
        <h2 className="text-2xl font-bold text-[var(--color-text-primary)]">
          서비스 안내
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 md:gap-6">
          {serviceInfo.map((info, index) => (
            <Card key={index} className="h-full">
              <div className="space-y-3">
                <div className="text-3xl">{info.icon}</div>
                <h3 className="text-lg font-semibold text-[var(--color-text-primary)]">
                  {info.title}
                </h3>
                <p className="text-sm text-[var(--color-text-secondary)] leading-relaxed">
                  {info.description}
                </p>
              </div>
            </Card>
          ))}
        </div>
      </section>
    </div>
  );
}

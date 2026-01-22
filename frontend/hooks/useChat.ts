"use client";

import { useState, useCallback } from "react";
import type { Message } from "@/components/chat/ChatArea";
import apiClient from "@/lib/api";

export const useChat = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const sendMessage = useCallback(async (content: string) => {
    // 사용자 메시지 추가
    const userMessage: Message = {
      id: `user-${Date.now()}`,
      role: "user",
      content,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    try {
      // 백엔드 API 호출
      const response = await apiClient.post("/api/v1/chat", {
        question: content,
      });
      const data = response.data;

      const botMessage: Message = {
        id: `bot-${Date.now()}`,
        role: "bot",
        content: data.answer,
        timestamp: new Date(),
        source: data.source || "AI 신입생 도우미",
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      console.error("메시지 전송 오류:", error);
      const errorMessage: Message = {
        id: `error-${Date.now()}`,
        role: "bot",
        content:
          "죄송해요. 일시적인 오류가 발생했어요. 백엔드 서버가 실행 중인지 확인해주세요.",
        timestamp: new Date(),
        source: "시스템",
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  }, []);

  return {
    messages,
    sendMessage,
    isLoading,
  };
};

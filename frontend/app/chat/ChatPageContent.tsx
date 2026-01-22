"use client";

import React, { useEffect } from "react";
import { useSearchParams } from "next/navigation";
import { ChatArea } from "@/components/chat/ChatArea";
import { InputArea } from "@/components/chat/InputArea";
import { useChat } from "@/hooks/useChat";

export function ChatPageContent() {
  const searchParams = useSearchParams();
  const initialQuestion = searchParams.get("q") || "";
  const { messages, sendMessage, isLoading } = useChat();

  useEffect(() => {
    if (initialQuestion && messages.length === 0) {
      sendMessage(initialQuestion);
    }
  }, [initialQuestion, messages.length, sendMessage]);

  return (
    <div className="flex flex-col h-[calc(100vh-12rem)] max-h-[800px]">
      <div className="flex-1 overflow-hidden">
        <ChatArea messages={messages} isLoading={isLoading} />
      </div>
      <div className="border-t border-[var(--color-border-primary)] pt-4">
        <InputArea onSendMessage={sendMessage} isLoading={isLoading} />
      </div>
    </div>
  );
}

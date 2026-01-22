"use client";

import React from "react";
import { UserMessage } from "./UserMessage";
import { BotMessage } from "./BotMessage";
import type { Message } from "./ChatArea";

export interface MessageListProps {
  messages: Message[];
}

export const MessageList: React.FC<MessageListProps> = ({ messages }) => {
  return (
    <div className="space-y-4">
      {messages.map((message) =>
        message.role === "user" ? (
          <UserMessage key={message.id} message={message} />
        ) : (
          <BotMessage key={message.id} message={message} />
        )
      )}
    </div>
  );
};

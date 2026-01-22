"use client";

import React, { Suspense } from "react";
import { ChatPageContent } from "./ChatPageContent";

export default function ChatPage() {
  return (
    <Suspense fallback={<div>로딩 중...</div>}>
      <ChatPageContent />
    </Suspense>
  );
}

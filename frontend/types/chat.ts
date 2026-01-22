export interface ChatRequest {
  question: string;
  context?: string[];
}

export interface ChatResponse {
  answer: string;
  source?: string;
  relatedQuestions?: string[];
}

export interface Message {
  id: string;
  role: "user" | "bot";
  content: string;
  timestamp: Date;
  source?: string;
}

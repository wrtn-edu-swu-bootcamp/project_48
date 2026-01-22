import { NextRequest, NextResponse } from "next/server";
import { processQuestionWithoutDB } from "@/lib/rag";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

interface ChatRequest {
  message?: string;
  question?: string;
}

export async function POST(request: NextRequest) {
  try {
    const body: ChatRequest = await request.json();
    const question = body.message || body.question;

    if (!question || typeof question !== "string") {
      return NextResponse.json(
        { error: "질문을 입력해주세요." },
        { status: 400 }
      );
    }

    console.log(`채팅 요청: ${question}`);

    // RAG 파이프라인 실행 (DB 없이 Gemini만 사용)
    const result = await processQuestionWithoutDB(question);

    return NextResponse.json({
      answer: result.answer,
      sources: result.sources,
      category: result.category,
    });
  } catch (error) {
    console.error("채팅 API 오류:", error);
    return NextResponse.json(
      {
        answer: "죄송해요. 일시적인 오류가 발생했어요. 잠시 후 다시 시도해주세요.",
        sources: [],
        category: "error",
      },
      { status: 500 }
    );
  }
}

export async function GET() {
  return NextResponse.json({
    message: "AI 신입생 도우미 채팅 API",
    usage: "POST /api/chat with { message: 'your question' }",
  });
}

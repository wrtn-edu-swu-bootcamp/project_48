import { GoogleGenerativeAI } from "@google/generative-ai";

// Gemini API 클라이언트 초기화
const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY || "");

// 모델 설정
const model = genAI.getGenerativeModel({
  model: "gemini-2.0-flash-exp",
  generationConfig: {
    temperature: 0.7,
    topP: 0.95,
    topK: 40,
    maxOutputTokens: 2048,
  },
});

// 시스템 프롬프트
const SYSTEM_PROMPT = `당신은 서울여자대학교 신입생을 돕는 친절한 AI 도우미입니다.

역할:
- 학사 일정, 수강신청, 등록금, 장학금, 휴학/복학 등 학사 정보 안내
- 공지사항 및 지원 프로그램 안내
- 학사 용어 설명

규칙:
1. 제공된 정보만을 기반으로 답변하세요
2. 정보가 없으면 "해당 정보는 현재 데이터에 없어요. 학교 행정실에 문의해주세요."라고 안내하세요
3. 친근하고 이해하기 쉬운 말투를 사용하세요 (존댓말 사용)
4. 답변은 명확하고 구조화되게 작성하세요
5. 중요한 날짜나 기한은 강조해서 알려주세요
6. 추측하지 마세요

답변 형식:
- 핵심 정보를 먼저 제공
- 필요시 관련 정보 추가 안내
- 추가 질문 유도`;

interface Context {
  source: string;
  title?: string;
  name?: string;
  term?: string;
  content?: string;
  description?: string;
  definition?: string;
}

/**
 * 컨텍스트를 포맷팅
 */
function formatContext(contexts: Context[]): string {
  if (!contexts.length) return "";

  let formatted = "다음은 참고할 정보입니다:\n\n";

  contexts.forEach((item, idx) => {
    formatted += `[문서 ${idx + 1}]\n`;
    formatted += `출처: ${item.source}\n`;

    if (item.title) formatted += `제목: ${item.title}\n`;
    if (item.name) formatted += `이름: ${item.name}\n`;
    if (item.term) formatted += `용어: ${item.term}\n`;

    if (item.content) formatted += `내용: ${item.content}\n`;
    else if (item.description) formatted += `설명: ${item.description}\n`;
    else if (item.definition) formatted += `정의: ${item.definition}\n`;

    formatted += "\n";
  });

  return formatted;
}

export interface GeminiResponse {
  answer: string;
  success: boolean;
  error?: string;
}

/**
 * Gemini API를 사용하여 응답 생성
 */
export async function generateResponse(
  userMessage: string,
  contexts: Context[] = []
): Promise<GeminiResponse> {
  try {
    // 컨텍스트가 있으면 메시지에 포함
    let fullMessage = userMessage;
    if (contexts.length > 0) {
      const contextText = formatContext(contexts);
      fullMessage = `${contextText}\n\n질문: ${userMessage}`;
    }

    // 프롬프트 생성
    const prompt = `${SYSTEM_PROMPT}\n\n${fullMessage}`;

    // Gemini API 호출
    const result = await model.generateContent(prompt);
    const response = result.response;
    const text = response.text();

    return {
      answer: text,
      success: true,
    };
  } catch (error) {
    console.error("Gemini API 오류:", error);
    return {
      answer: "죄송해요. 일시적인 오류가 발생했어요. 잠시 후 다시 시도해주세요.",
      success: false,
      error: error instanceof Error ? error.message : "Unknown error",
    };
  }
}

/**
 * 스트리밍 응답 생성
 */
export async function* generateStreamResponse(
  userMessage: string,
  contexts: Context[] = []
): AsyncGenerator<string> {
  try {
    let fullMessage = userMessage;
    if (contexts.length > 0) {
      const contextText = formatContext(contexts);
      fullMessage = `${contextText}\n\n질문: ${userMessage}`;
    }

    const prompt = `${SYSTEM_PROMPT}\n\n${fullMessage}`;

    const result = await model.generateContentStream(prompt);

    for await (const chunk of result.stream) {
      const text = chunk.text();
      if (text) {
        yield text;
      }
    }
  } catch (error) {
    console.error("Gemini Streaming 오류:", error);
    yield "죄송해요. 일시적인 오류가 발생했어요. 잠시 후 다시 시도해주세요.";
  }
}

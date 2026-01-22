import { generateResponse } from "./gemini";

interface SearchResult {
  source: string;
  title?: string;
  name?: string;
  term?: string;
  content?: string;
  description?: string;
  definition?: string;
  score?: number;
}

interface Source {
  name: string;
  url?: string;
}

interface RAGResult {
  answer: string;
  sources: Source[];
  category: string;
  success: boolean;
}

// 질문 카테고리 분류
type QuestionCategory = "학사일정" | "공지사항" | "지원프로그램" | "학사정보" | "기타";

const CATEGORY_KEYWORDS: Record<QuestionCategory, string[]> = {
  학사일정: [
    "수강신청", "등록금", "납부", "개강", "종강", "중간고사", "기말고사",
    "시험", "휴학", "복학", "계절학기", "언제", "일정", "기간"
  ],
  공지사항: [
    "공지", "안내", "알림", "소식", "발표"
  ],
  지원프로그램: [
    "장학금", "장학", "멘토링", "프로그램", "지원", "신청", "비교과",
    "마일리지", "동아리", "창업", "취업"
  ],
  학사정보: [
    "학점", "전공", "복수전공", "부전공", "교양", "이수", "졸업",
    "평점", "재수강", "뭐야", "뭔가요", "무엇", "어떻게"
  ],
  기타: []
};

/**
 * 질문 카테고리 분류
 */
function classifyQuestion(question: string): QuestionCategory {
  const normalizedQuestion = question.toLowerCase();
  
  let maxScore = 0;
  let bestCategory: QuestionCategory = "기타";
  
  for (const [category, keywords] of Object.entries(CATEGORY_KEYWORDS)) {
    if (category === "기타") continue;
    
    let score = 0;
    for (const keyword of keywords) {
      if (normalizedQuestion.includes(keyword.toLowerCase())) {
        score += 1;
      }
    }
    
    if (score > maxScore) {
      maxScore = score;
      bestCategory = category as QuestionCategory;
    }
  }
  
  return bestCategory;
}

// 내장 데이터 (JSON 기반)
const SCHEDULES = [
  { name: "1학기 수강신청", startDate: "2025-02-25", endDate: "2025-02-28", description: "2025학년도 1학기 수강신청 기간" },
  { name: "1학기 등록금 납부", startDate: "2025-02-10", endDate: "2025-02-17", description: "등록금 납부 기간" },
  { name: "1학기 개강", startDate: "2025-03-03", description: "1학기 개강일" },
  { name: "1학기 중간고사", startDate: "2025-04-21", endDate: "2025-04-25", description: "중간고사 기간" },
  { name: "1학기 기말고사", startDate: "2025-06-16", endDate: "2025-06-20", description: "기말고사 기간" },
];

const GLOSSARY = [
  { termKo: "학점제", definition: "과목을 수강하여 일정 학점을 취득해야 졸업할 수 있는 제도" },
  { termKo: "복수전공", definition: "두 개의 전공을 동시에 이수하는 것" },
  { termKo: "부전공", definition: "전공 외에 추가로 선택하는 보조 전공" },
  { termKo: "수강신청", definition: "원하는 과목을 선택하여 신청하는 것" },
  { termKo: "휴학", definition: "일정 기간 동안 학업을 중단하는 것" },
  { termKo: "평점평균", definition: "모든 과목의 평균 점수 (4.5 만점)" },
  { termKo: "캠퍼스 마일리지", definition: "다양한 활동으로 마일리지를 적립하여 장학금 수혜 가능" },
];

const PROGRAMS = [
  { name: "국가장학금", description: "한국장학재단에서 지원하는 장학금" },
  { name: "학교 내부 장학금", description: "학교 자체 예산으로 지원하는 장학금" },
  { name: "학생성장지원시스템", description: "비교과 활동, 진로·취업, 상담 통합 관리 시스템" },
  { name: "온라인 동문 멘토링", description: "졸업 동문과의 1:1 멘토링" },
];

/**
 * 키워드 기반 검색 (내장 데이터 사용)
 */
function searchByKeywords(
  query: string,
  category: QuestionCategory,
  limit: number = 5
): SearchResult[] {
  const results: SearchResult[] = [];
  const keywords = query.toLowerCase().split(/\s+/).filter(k => k.length > 1);
  
  // 학사 일정 검색
  if (category === "학사일정" || category === "기타") {
    SCHEDULES.forEach(schedule => {
      const text = `${schedule.name} ${schedule.description}`.toLowerCase();
      if (keywords.some(k => text.includes(k))) {
        results.push({
          source: "학사일정",
          name: schedule.name,
          description: schedule.description,
          content: `${schedule.name}: ${schedule.startDate}${schedule.endDate ? ` ~ ${schedule.endDate}` : ""}`
        });
      }
    });
  }
  
  // 학사 용어 검색
  if (category === "학사정보" || category === "기타") {
    GLOSSARY.forEach(term => {
      const text = `${term.termKo} ${term.definition}`.toLowerCase();
      if (keywords.some(k => text.includes(k))) {
        results.push({
          source: "학사용어",
          term: term.termKo,
          definition: term.definition
        });
      }
    });
  }
  
  // 지원 프로그램 검색
  if (category === "지원프로그램" || category === "기타") {
    PROGRAMS.forEach(program => {
      const text = `${program.name} ${program.description}`.toLowerCase();
      if (keywords.some(k => text.includes(k))) {
        results.push({
          source: "지원프로그램",
          name: program.name,
          description: program.description
        });
      }
    });
  }
  
  return results.slice(0, limit);
}

/**
 * RAG 파이프라인 실행
 */
export async function processQuestion(question: string): Promise<RAGResult> {
  try {
    // 1. 질문 분류
    const category = classifyQuestion(question);
    console.log(`질문 카테고리: ${category}`);
    
    // 2. 관련 정보 검색 (내장 데이터 사용)
    const searchResults = searchByKeywords(question, category, 5);
    console.log(`검색 결과 수: ${searchResults.length}`);
    
    // 3. Gemini API로 답변 생성
    const geminiResult = await generateResponse(question, searchResults);
    
    // 4. 출처 정보 추출
    const sources: Source[] = [];
    const seenSources = new Set<string>();
    
    searchResults.forEach(result => {
      if (!seenSources.has(result.source)) {
        sources.push({ name: result.source });
        seenSources.add(result.source);
      }
    });
    
    return {
      answer: geminiResult.answer,
      sources,
      category,
      success: geminiResult.success
    };
  } catch (error) {
    console.error("RAG 파이프라인 오류:", error);
    return {
      answer: "죄송해요. 일시적인 오류가 발생했어요. 잠시 후 다시 시도해주세요.",
      sources: [],
      category: "기타",
      success: false
    };
  }
}

/**
 * 폴백 응답 생성 (DB 없이)
 */
export async function processQuestionWithoutDB(question: string): Promise<RAGResult> {
  try {
    const category = classifyQuestion(question);
    const geminiResult = await generateResponse(question, []);
    
    return {
      answer: geminiResult.answer,
      sources: [],
      category,
      success: geminiResult.success
    };
  } catch (error) {
    console.error("RAG 오류:", error);
    return {
      answer: "죄송해요. 일시적인 오류가 발생했어요. 잠시 후 다시 시도해주세요.",
      sources: [],
      category: "기타",
      success: false
    };
  }
}

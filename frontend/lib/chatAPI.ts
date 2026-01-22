import apiClient from "./api";

export interface ChatRequest {
  question: string;
  context?: string[];
}

export interface Source {
  name: string;
  url?: string;
}

export interface ChatResponse {
  answer: string;
  sources?: Source[];
  category?: string;
  related_questions?: string[];
}

export const chatAPI = {
  /**
   * 질문을 전송하고 답변을 받습니다
   */
  async sendMessage(question: string): Promise<ChatResponse> {
    const response = await apiClient.post<ChatResponse>("/api/chat", {
      message: question,
    });
    return response.data;
  },

  /**
   * 피드백을 전송합니다
   */
  async sendFeedback(
    messageId: string,
    feedback: "positive" | "negative",
    comment?: string
  ): Promise<void> {
    // TODO: 피드백 API 구현 예정
    console.log("Feedback:", { messageId, feedback, comment });
  },
};

export const scheduleAPI = {
  /**
   * 학사 일정 목록을 가져옵니다
   */
  async getSchedules(semester?: string, scheduleType?: string) {
    const params = new URLSearchParams();
    if (semester) params.append("semester", semester);
    if (scheduleType) params.append("schedule_type", scheduleType);
    
    const response = await apiClient.get(`/api/schedules?${params.toString()}`);
    return response.data;
  },

  /**
   * 특정 학사 일정을 가져옵니다
   */
  async getSchedule(id: number) {
    const response = await apiClient.get(`/api/schedules/${id}`);
    return response.data;
  },
};

export const noticeAPI = {
  /**
   * 공지사항 목록을 가져옵니다
   */
  async getNotices(category?: string, limit = 20, offset = 0) {
    const params = new URLSearchParams();
    if (category) params.append("category", category);
    params.append("limit", String(limit));
    params.append("offset", String(offset));
    
    const response = await apiClient.get(`/api/notices?${params.toString()}`);
    return response.data;
  },

  /**
   * 특정 공지사항을 가져옵니다
   */
  async getNotice(id: number) {
    const response = await apiClient.get(`/api/notices/${id}`);
    return response.data;
  },
};

export const programAPI = {
  /**
   * 지원 프로그램 목록을 가져옵니다
   */
  async getPrograms(programType?: string, limit = 20, offset = 0) {
    const params = new URLSearchParams();
    if (programType) params.append("program_type", programType);
    params.append("limit", String(limit));
    params.append("offset", String(offset));
    
    const response = await apiClient.get(`/api/programs?${params.toString()}`);
    return response.data;
  },

  /**
   * 특정 지원 프로그램을 가져옵니다
   */
  async getProgram(id: number) {
    const response = await apiClient.get(`/api/programs/${id}`);
    return response.data;
  },
};

import axios from "axios";

// Vercel 배포 시 내부 API Routes 사용
const apiClient = axios.create({
  baseURL: "", // 내부 API Routes 사용 (상대 경로)
  headers: {
    "Content-Type": "application/json",
  },
});

// 요청 인터셉터
apiClient.interceptors.request.use(
  (config) => {
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 응답 인터셉터
apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response) {
      // 서버 응답 오류
      console.error("API 오류:", error.response.data);
    } else if (error.request) {
      // 요청은 보냈지만 응답을 받지 못함
      console.error("네트워크 오류:", error.request);
    } else {
      // 요청 설정 중 오류
      console.error("오류:", error.message);
    }
    return Promise.reject(error);
  }
);

export default apiClient;

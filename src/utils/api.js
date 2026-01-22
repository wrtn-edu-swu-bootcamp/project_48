/**
 * API 호출 함수
 * 추후 실제 챗봇 API와 연동할 수 있도록 구조 설계
 */

const API_BASE_URL = process.env.REACT_APP_API_URL || '/api';

/**
 * 챗봇 메시지 전송
 * @param {string} message - 사용자 메시지
 * @returns {Promise<Object>} 봇 응답 객체
 */
export async function sendChatMessage(message) {
  // TODO: 실제 API 엔드포인트로 교체
  // const response = await fetch(`${API_BASE_URL}/chat`, {
  //   method: 'POST',
  //   headers: {
  //     'Content-Type': 'application/json',
  //   },
  //   body: JSON.stringify({ message }),
  // });
  // return await response.json();

  // 현재는 모의 응답 (개발/테스트용)
  return new Promise((resolve) => {
    setTimeout(() => {
      // 간단한 키워드 기반 응답 (실제로는 AI 모델로 교체)
      let responseText = '';
      let source = '';

      if (message.includes('수강신청')) {
        responseText = `수강신청 일정 안내

서울여자대학교의 수강신청 일정은 다음과 같습니다:

• 1학기: 개강 직전 및 개강 초기 정정 기간
• 2학기: 8월 초 (예: 8월 3일~7일)
• 수강신청 확인 및 정정 기간: 개강 직후

다음 행동 가이드:
- 수강신청 전에 수강 계획을 미리 준비하세요
- 학점 제한을 확인하세요 (최소 10학점, 최대 18학점)
- 성적 우수자(평점 3.6 이상)는 최대 21학점 신청 가능`;
        source = '2025학년도 학사일정';
      } else if (message.includes('장학금')) {
        responseText = `장학금 신청 안내

서울여자대학교에서는 다양한 장학금 프로그램을 운영하고 있습니다:

• 교외장학금: 외국교환학생 선발자 등
• 국가장학금: 국가보훈자녀, 북한이탈주민 자녀 등
• 학교 내부 장학: 성적 우수 + 가정 형편 고려

다음 행동 가이드:
- 학생성장지원시스템에서 신청 가능한 장학금 확인
- 신청 기간과 자격 요건을 확인하세요
- 필요 서류를 미리 준비하세요`;
        source = '학생처 공지사항';
      } else if (message.includes('용어')) {
        responseText = `학사 용어 안내

궁금하신 학사 용어를 알려주시면 쉽게 설명해드릴게요!

주요 학사 용어:
• 학점제: 과목을 수강하여 일정 학점을 취득해야 졸업할 수 있는 제도
• 전공: 본인이 선택한 전문 분야
• 복수전공: 두 개의 전공을 동시에 이수하는 것
• 부전공: 전공 외에 추가로 선택하는 보조 전공

어떤 용어가 궁금하신가요?`;
        source = '학사 용어 사전';
      } else {
        responseText = `안녕하세요! AI 신입생 도우미입니다.

학사 일정, 공지사항, 지원 프로그램에 대해 궁금한 점을 물어보세요.

예를 들어:
• "수강신청은 언제 하나요?"
• "장학금 신청 방법이 궁금해요"
• "학사 용어가 어려워요"

어떤 것이 궁금하신가요?`;
        source = 'AI 신입생 도우미';
      }

      resolve({
        text: responseText,
        source: source,
      });
    }, 1000); // 1초 지연 (실제 API 호출 시뮬레이션)
  });
}

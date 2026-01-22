import { NextRequest, NextResponse } from "next/server";

export const runtime = "nodejs";

// 공지사항 데이터 (JSON 기반)
const notices = [
  {
    id: 1,
    title: "2025학년도 1학기 수강신청 안내",
    content: "2025학년도 1학기 수강신청을 다음과 같이 안내합니다.\n\n• 수강신청 기간: 2025. 2. 25(화) ~ 2. 28(금)\n• 수강신청 정정 기간: 2025. 3. 3(월) ~ 3. 7(금)\n• 학점 제한: 최소 10학점, 최대 18학점 (성적 우수자 21학점)\n• 수강신청은 학사시스템을 통해 진행됩니다.",
    noticeType: "학사",
    importance: "높음",
    department: "학사지원팀"
  },
  {
    id: 2,
    title: "2025학년도 1학기 등록금 납부 안내",
    content: "2025학년도 1학기 등록금 납부 기간을 안내합니다.\n\n• 납부 기간: 2025. 2. 10(월) ~ 2. 17(월)\n• 납부 방법: 가상계좌 또는 학교 방문 납부\n• 분할납부 신청 가능 (한국장학재단 학자금대출 신청자)\n• 기한 내 미납 시 제적 처리될 수 있으니 유의하시기 바랍니다.",
    noticeType: "등록금",
    importance: "높음",
    department: "재무팀"
  },
  {
    id: 3,
    title: "2025학년도 1학기 장학금 신청 안내",
    content: "2025학년도 1학기 장학금 신청을 안내합니다.\n\n• 신청 기간: 2025. 2. 1(토) ~ 2. 20(목)\n• 신청 방법: 학생성장지원시스템을 통한 온라인 신청\n• 대상: 전체 재학생 (성적, 가정형편 등 고려)\n• 문의: 학생지원팀 (02-970-XXXX)",
    noticeType: "장학금",
    importance: "높음",
    department: "학생지원팀"
  },
  {
    id: 4,
    title: "학생성장지원시스템 비교과 프로그램 안내",
    content: "학생성장지원시스템을 통한 비교과 프로그램 신청을 안내합니다.\n\n• 프로그램: 진로탐색, 취업준비, 역량강화 등\n• 신청: 학생성장지원시스템에서 상시 신청 가능\n• 마일리지 적립 및 장학금 연계\n• 자세한 사항은 학생성장지원시스템을 참고하세요.",
    noticeType: "비교과 프로그램",
    importance: "보통",
    department: "학생성장지원센터"
  },
  {
    id: 5,
    title: "국가장학금 신청 안내",
    content: "2025학년도 1학기 국가장학금 신청을 안내합니다.\n\n• 신청 기간: 한국장학재단 홈페이지 참고\n• 대상: 소득 8분위 이하 대학생\n• 신청 방법: 한국장학재단 홈페이지 (www.kosaf.go.kr)\n• 주의: 반드시 기한 내 신청해야 함",
    noticeType: "장학금",
    importance: "높음",
    department: "학생지원팀"
  },
  {
    id: 6,
    title: "수강중도포기 제도 안내",
    content: "수강중도포기 제도를 안내합니다.\n\n• 신청 기간: 중간고사 이후 ~ 기말고사 2주 전\n• 대상: 전체 재학생 (학기당 1과목)\n• 신청 방법: 학사시스템 온라인 신청\n• 효과: W 표기 (성적 평점에 포함되지 않음)\n• 주의: 최소 학점 (10학점)을 충족해야 함",
    noticeType: "학사",
    importance: "보통",
    department: "학사지원팀"
  }
];

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const category = searchParams.get("category");
  const limit = parseInt(searchParams.get("limit") || "20");
  const offset = parseInt(searchParams.get("offset") || "0");

  let filtered = notices;

  if (category) {
    filtered = filtered.filter(n => n.noticeType === category);
  }

  const paged = filtered.slice(offset, offset + limit);

  return NextResponse.json({
    notices: paged,
    total: filtered.length,
    limit,
    offset
  });
}

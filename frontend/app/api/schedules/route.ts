import { NextRequest, NextResponse } from "next/server";

export const runtime = "nodejs";

// 학사 일정 데이터 (JSON 기반)
const schedules = [
  {
    id: 1,
    name: "1학기 수강신청",
    startDate: "2025-02-25",
    endDate: "2025-02-28",
    semester: "1학기",
    scheduleType: "수강신청",
    description: "2025학년도 1학기 수강신청 기간입니다. 재학생 대상이며, 학년별로 시간이 다릅니다.",
    importance: 10
  },
  {
    id: 2,
    name: "1학기 수강신청 정정",
    startDate: "2025-03-03",
    endDate: "2025-03-07",
    semester: "1학기",
    scheduleType: "수강신청",
    description: "개강 후 수강신청 정정 기간입니다. 과목 변경이 가능합니다.",
    importance: 9
  },
  {
    id: 3,
    name: "1학기 등록금 납부",
    startDate: "2025-02-10",
    endDate: "2025-02-17",
    semester: "1학기",
    scheduleType: "등록금 납부",
    description: "1학기 등록금 납부 기간입니다. 기한 내 납부하지 않으면 제적될 수 있습니다.",
    importance: 10
  },
  {
    id: 4,
    name: "1학기 개강",
    startDate: "2025-03-03",
    endDate: "2025-03-03",
    semester: "1학기",
    scheduleType: "기타",
    description: "2025학년도 1학기 개강일입니다.",
    importance: 8
  },
  {
    id: 5,
    name: "1학기 중간고사",
    startDate: "2025-04-21",
    endDate: "2025-04-25",
    semester: "1학기",
    scheduleType: "시험",
    description: "1학기 중간고사 기간입니다.",
    importance: 9
  },
  {
    id: 6,
    name: "1학기 기말고사",
    startDate: "2025-06-16",
    endDate: "2025-06-20",
    semester: "1학기",
    scheduleType: "시험",
    description: "1학기 기말고사 기간입니다.",
    importance: 9
  },
  {
    id: 7,
    name: "여름 계절학기 등록",
    startDate: "2025-06-08",
    endDate: "2025-06-12",
    semester: "여름 계절학기",
    scheduleType: "수강신청",
    description: "여름 계절학기 수강신청 기간입니다.",
    importance: 7
  },
  {
    id: 8,
    name: "1학기 휴학 신청",
    startDate: "2025-02-15",
    endDate: "2025-03-07",
    semester: "1학기",
    scheduleType: "휴학/복학",
    description: "1학기 휴학 신청 기간입니다. 학사시스템에서 신청 가능합니다.",
    importance: 8
  },
  {
    id: 9,
    name: "2학기 수강신청",
    startDate: "2025-08-03",
    endDate: "2025-08-07",
    semester: "2학기",
    scheduleType: "수강신청",
    description: "2025학년도 2학기 수강신청 기간입니다.",
    importance: 10
  },
  {
    id: 10,
    name: "2학기 개강",
    startDate: "2025-09-01",
    endDate: "2025-09-01",
    semester: "2학기",
    scheduleType: "기타",
    description: "2025학년도 2학기 개강일입니다.",
    importance: 8
  }
];

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const semester = searchParams.get("semester");
  const scheduleType = searchParams.get("schedule_type");

  let filtered = schedules;

  if (semester) {
    filtered = filtered.filter(s => s.semester === semester);
  }

  if (scheduleType) {
    filtered = filtered.filter(s => s.scheduleType === scheduleType);
  }

  // 중요도 순으로 정렬
  filtered.sort((a, b) => b.importance - a.importance);

  return NextResponse.json({
    schedules: filtered,
    total: filtered.length
  });
}

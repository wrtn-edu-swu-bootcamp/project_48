import { NextRequest, NextResponse } from "next/server";

export const runtime = "nodejs";

// 지원 프로그램 데이터 (JSON 기반)
const programs = [
  {
    id: 1,
    name: "교외장학금",
    programType: "장학금",
    applicationStart: "2025-02-01",
    applicationEnd: "2025-02-20",
    target: "외국교환학생 선발자, 우수한 학업성적 및 경제적 여건 고려",
    applicationMethod: "학생성장지원시스템을 통한 온라인 신청",
    requirements: "외국교환학생 선발자 또는 우수 성적 및 가정형편 고려",
    documents: "장학금 신청서, 성적증명서, 가족관계증명서 등",
    benefits: "등록금 일부 또는 전액 지원",
    description: "외국교환학생 선발자 및 우수한 학업성적을 가진 학생에게 지원하는 장학금입니다."
  },
  {
    id: 2,
    name: "국가장학금",
    programType: "장학금",
    applicationStart: "2025-01-15",
    applicationEnd: "2025-02-28",
    target: "국가보훈자녀, 북한이탈주민 자녀 등 특별 대상자",
    applicationMethod: "한국장학재단 홈페이지 (www.kosaf.go.kr) 신청",
    requirements: "국가보훈대상자 또는 북한이탈주민 자녀",
    documents: "국가보훈대상자 증명서 또는 북한이탈주민 확인서",
    benefits: "등록금 전액 또는 일부 지원",
    description: "국가에서 지원하는 장학금으로, 특별 대상자에게 지원됩니다."
  },
  {
    id: 3,
    name: "학교 내부 장학금",
    programType: "장학금",
    applicationStart: "2025-02-01",
    applicationEnd: "2025-02-20",
    target: "성적 우수자 및 가정 형편을 고려한 재학생",
    applicationMethod: "학생성장지원시스템을 통한 온라인 신청",
    requirements: "평점 평균 3.0 이상 및 가정형편 고려",
    documents: "장학금 신청서, 성적증명서, 가족관계증명서, 소득증명서 등",
    benefits: "등록금 일부 지원 (학기당 50만원~200만원)",
    description: "학교 자체 예산으로 지원하는 장학금입니다."
  },
  {
    id: 4,
    name: "학생성장지원시스템",
    programType: "비교과 프로그램",
    target: "전체 재학생",
    applicationMethod: "학생성장지원시스템 온라인 신청",
    requirements: "재학생",
    documents: "없음 (온라인 신청만)",
    benefits: "비교과 활동 기록, 마일리지 적립, 핵심역량 진단",
    description: "비교과 활동, 진로·취업, 상담을 통합 관리하는 시스템입니다. 마일리지 적립 시 장학금 수혜 가능성이 높아집니다."
  },
  {
    id: 5,
    name: "SWU-SI 사회혁신 프로젝트",
    programType: "비교과 프로그램",
    applicationStart: "2025-03-10",
    applicationEnd: "2025-03-20",
    target: "사회문제에 관심있는 재학생",
    applicationMethod: "SWU-SI 센터 홈페이지 신청",
    requirements: "재학생, 사회문제 해결에 대한 관심",
    documents: "프로젝트 계획서, 팀 구성서",
    benefits: "프로젝트 지원금, 멘토링, 마일리지 적립",
    description: "사회혁신자를 양성하기 위한 교과-비교과 연계 교육과정입니다."
  },
  {
    id: 6,
    name: "온라인 동문 멘토링",
    programType: "멘토링",
    applicationStart: "2025-03-01",
    applicationEnd: "2025-03-15",
    target: "전체 재학생",
    applicationMethod: "학생성장지원시스템 신청",
    requirements: "재학생",
    documents: "멘토링 신청서",
    benefits: "1:1 멘토링, 진로·취업 상담, 마일리지 적립",
    description: "졸업 동문과의 온라인 멘토링 프로그램입니다."
  },
  {
    id: 7,
    name: "캠퍼스 마일리지 제도",
    programType: "기타",
    target: "전체 재학생",
    applicationMethod: "자동 적립 (학생성장지원시스템)",
    requirements: "재학생, 비교과 활동 참여",
    documents: "없음",
    benefits: "마일리지 적립 시 장학금 수혜 가능성 향상",
    description: "학생의 다양한 활동 및 학업 성취도를 마일리지로 적립하여 장학금 수혜 가능하게 하는 제도입니다."
  }
];

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const programType = searchParams.get("program_type");
  const limit = parseInt(searchParams.get("limit") || "20");
  const offset = parseInt(searchParams.get("offset") || "0");

  let filtered = programs;

  if (programType) {
    filtered = filtered.filter(p => p.programType === programType);
  }

  const paged = filtered.slice(offset, offset + limit);

  return NextResponse.json({
    programs: paged,
    total: filtered.length,
    limit,
    offset
  });
}

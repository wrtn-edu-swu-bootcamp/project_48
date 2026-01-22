#!/usr/bin/env python3
"""
데이터베이스 초기화 스크립트
"""
import sys
import os

# 프로젝트 루트 디렉토리를 Python 경로에 추가
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.core.database import engine, Base
from app.models import (
    academic_schedule,
    notice,
    support_program,
    academic_term,
    question_log
)

def init_database():
    """데이터베이스 초기화"""
    print("데이터베이스 초기화 중...")

    try:
        # 모든 테이블 생성
        Base.metadata.create_all(bind=engine)
        print("✅ 데이터베이스 테이블 생성 완료")

        # 샘플 데이터 추가 (개발용)
        add_sample_data()

        print("✅ 데이터베이스 초기화 완료")

    except Exception as e:
        print(f"❌ 데이터베이스 초기화 실패: {e}")
        sys.exit(1)

def add_sample_data():
    """샘플 데이터 추가"""
    from sqlalchemy.orm import sessionmaker
    from datetime import date, datetime
    from app.models.academic_schedule import AcademicSchedule, SemesterType, ScheduleType
    from app.models.notice import Notice, NoticeType, ImportanceLevel
    from app.models.support_program import SupportProgram, ProgramType
    from app.models.academic_term import AcademicTerm
    from app.models.question_log import QuestionLog, QuestionStatus, QuestionCategory

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    try:
        # 학사 일정 샘플 데이터
        if not db.query(AcademicSchedule).first():
            schedules = [
                AcademicSchedule(
                    name="2025학년도 1학기 수강신청",
                    start_date=date(2025, 2, 10),
                    end_date=date(2025, 2, 14),
                    semester=SemesterType.FIRST,
                    schedule_type=ScheduleType.COURSE_REGISTRATION,
                    description="1학기 수강신청 기간입니다. 학사정보시스템에서 신청하세요.",
                    importance=9,
                    created_at=date.today(),
                ),
                AcademicSchedule(
                    name="2025학년도 1학기 등록금 납부",
                    start_date=date(2025, 2, 20),
                    end_date=date(2025, 2, 25),
                    semester=SemesterType.FIRST,
                    schedule_type=ScheduleType.TUITION_PAYMENT,
                    description="등록금 납부 기간입니다. 기한 내 납부하지 않으면 수강신청이 취소됩니다.",
                    importance=10,
                    created_at=date.today(),
                ),
            ]
            db.add_all(schedules)
            print("✅ 학사 일정 샘플 데이터 추가됨")

        # 공지사항 샘플 데이터
        if not db.query(Notice).first():
            notices = [
                Notice(
                    title="2025학년도 장학금 신청 안내",
                    content="2025학년도 국가장학금 및 교내 장학금 신청 기간입니다. 자세한 사항은 학생지원팀으로 문의하세요.",
                    notice_type=NoticeType.SCHOLARSHIP,
                    importance=ImportanceLevel.HIGH,
                    department="학생지원팀",
                    created_at=date.today(),
                ),
                Notice(
                    title="수강신청 시스템 점검 안내",
                    content="2025년 2월 15일 오후 2시부터 4시까지 학사정보시스템 점검이 있을 예정입니다.",
                    notice_type=NoticeType.ACADEMIC,
                    importance=ImportanceLevel.MEDIUM,
                    department="정보화본부",
                    created_at=date.today(),
                ),
            ]
            db.add_all(notices)
            print("✅ 공지사항 샘플 데이터 추가됨")

        # 지원 프로그램 샘플 데이터
        if not db.query(SupportProgram).first():
            programs = [
                SupportProgram(
                    name="성적우수장학금",
                    program_type=ProgramType.SCHOLARSHIP,
                    application_start=date(2025, 3, 1),
                    application_end=date(2025, 3, 15),
                    target="전체 재학생",
                    application_method="온라인 신청 (학사정보시스템)",
                    requirements="직전 학기 평점 3.5 이상",
                    benefits="등록금 전액 또는 50% 지원",
                    description="학업 성적이 우수한 학생에게 지급되는 장학금입니다.",
                    created_at=date.today(),
                ),
                SupportProgram(
                    name="비교과 프로그램 참여 장려 장학금",
                    program_type=ProgramType.EXTRACURRICULAR,
                    application_start=date(2025, 4, 1),
                    application_end=date(2025, 4, 30),
                    target="1학년 재학생",
                    application_method="학생지원팀 방문 신청",
                    requirements="비교과 프로그램 2회 이상 참여",
                    benefits="등록금 30% 지원",
                    description="다양한 비교과 활동에 참여하는 학생을 장려하기 위한 장학금입니다.",
                    created_at=date.today(),
                ),
            ]
            db.add_all(programs)
            print("✅ 지원 프로그램 샘플 데이터 추가됨")

        # 학사 용어 샘플 데이터
        if not db.query(AcademicTerm).first():
            terms = [
                AcademicTerm(
                    term="수강신청",
                    definition="학생이 희망하는 강의를 선택하여 등록하는 절차",
                    easy_explanation="원하는 과목을 골라서 듣겠다고 신청하는 것",
                    example="매 학기 초에 진행되는 수강신청 기간에 학사정보시스템에서 과목을 선택합니다.",
                    created_at=date.today(),
                ),
                AcademicTerm(
                    term="등록금",
                    definition="대학 교육을 받는 대가로 납부하는 금액",
                    easy_explanation="학교 다니는 비용",
                    example="학기당 등록금은 학과와 학년별로 차이가 있습니다.",
                    created_at=date.today(),
                ),
            ]
            db.add_all(terms)
            print("✅ 학사 용어 샘플 데이터 추가됨")

        db.commit()

    except Exception as e:
        print(f"❌ 샘플 데이터 추가 실패: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_database()
"""
데이터베이스 초기 데이터 입력 스크립트
"""
import sys
import os
import json
from datetime import datetime, date
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine, Base
from app.models import (
    AcademicSchedule, SemesterType, ScheduleType,
    Notice, NoticeType, ImportanceLevel,
    SupportProgram, ProgramType,
    AcademicGlossary
)


def load_json_data(filename: str):
    """JSON 파일 로드"""
    data_dir = Path(__file__).parent / "data"
    with open(data_dir / filename, 'r', encoding='utf-8') as f:
        return json.load(f)


def seed_academic_schedules(db: Session):
    """학사 일정 데이터 삽입"""
    print("학사 일정 데이터 삽입 중...")
    data = load_json_data("academic_schedules.json")
    
    for item in data:
        schedule = AcademicSchedule(
            name=item["name"],
            start_date=datetime.strptime(item["start_date"], "%Y-%m-%d").date(),
            end_date=datetime.strptime(item["end_date"], "%Y-%m-%d").date() if item["end_date"] else None,
            semester=SemesterType(item["semester"]),
            schedule_type=ScheduleType(item["schedule_type"]),
            description=item.get("description"),
            importance=item.get("importance", 5),
            created_at=date.today()
        )
        db.add(schedule)
    
    db.commit()
    print(f"✓ 학사 일정 {len(data)}개 삽입 완료")


def seed_notices(db: Session):
    """공지사항 데이터 삽입"""
    print("공지사항 데이터 삽입 중...")
    data = load_json_data("notices.json")
    
    for item in data:
        notice = Notice(
            title=item["title"],
            content=item["content"],
            notice_type=NoticeType(item["notice_type"]),
            importance=ImportanceLevel(item["importance"]),
            department=item.get("department"),
            created_at=date.today(),
            is_active=1
        )
        db.add(notice)
    
    db.commit()
    print(f"✓ 공지사항 {len(data)}개 삽입 완료")


def seed_support_programs(db: Session):
    """지원 프로그램 데이터 삽입"""
    print("지원 프로그램 데이터 삽입 중...")
    data = load_json_data("support_programs.json")
    
    for item in data:
        program = SupportProgram(
            name=item["name"],
            program_type=ProgramType(item["program_type"]),
            application_start=datetime.strptime(item["application_start"], "%Y-%m-%d").date() if item.get("application_start") else None,
            application_end=datetime.strptime(item["application_end"], "%Y-%m-%d").date() if item.get("application_end") else None,
            target=item.get("target"),
            application_method=item.get("application_method"),
            requirements=item.get("requirements"),
            documents=item.get("documents"),
            benefits=item.get("benefits"),
            description=item.get("description"),
            created_at=date.today(),
            is_active=1
        )
        db.add(program)
    
    db.commit()
    print(f"✓ 지원 프로그램 {len(data)}개 삽입 완료")


def seed_glossary(db: Session):
    """학사 용어 사전 데이터 삽입"""
    print("학사 용어 사전 데이터 삽입 중...")
    data = load_json_data("glossary.json")
    
    for item in data:
        glossary = AcademicGlossary(
            term_ko=item["term_ko"],
            term_en=item.get("term_en"),
            definition=item["definition"],
            examples=item.get("examples"),
            category=item.get("category"),
            created_at=date.today()
        )
        db.add(glossary)
    
    db.commit()
    print(f"✓ 학사 용어 {len(data)}개 삽입 완료")


def main():
    """메인 함수"""
    print("=" * 50)
    print("데이터베이스 초기 데이터 입력 시작")
    print("=" * 50)
    
    # 데이터베이스 세션 생성
    db = SessionLocal()
    
    try:
        # 각 테이블에 데이터 삽입
        seed_academic_schedules(db)
        seed_notices(db)
        seed_support_programs(db)
        seed_glossary(db)
        
        print("=" * 50)
        print("✓ 모든 초기 데이터 입력 완료!")
        print("=" * 50)
        
    except Exception as e:
        print(f"✗ 오류 발생: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()

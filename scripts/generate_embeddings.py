"""
기존 데이터에 대한 임베딩 생성 스크립트
"""
import sys
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.services.ai.embeddings import get_embedding_service
from app.models import AcademicSchedule, Notice, SupportProgram, AcademicGlossary
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def generate_embeddings_for_schedules(db: Session, embedding_service):
    """학사 일정 임베딩 생성"""
    logger.info("학사 일정 임베딩 생성 중...")
    schedules = db.query(AcademicSchedule).filter(AcademicSchedule.embedding == None).all()
    
    for schedule in schedules:
        # 이름 + 설명을 합쳐서 임베딩 생성
        text = f"{schedule.name}. {schedule.description or ''}"
        embedding = embedding_service.get_embedding(text)
        schedule.embedding = embedding
    
    db.commit()
    logger.info(f"✓ 학사 일정 {len(schedules)}개 임베딩 생성 완료")


def generate_embeddings_for_notices(db: Session, embedding_service):
    """공지사항 임베딩 생성"""
    logger.info("공지사항 임베딩 생성 중...")
    notices = db.query(Notice).filter(Notice.embedding == None).all()
    
    for notice in notices:
        # 제목 + 내용을 합쳐서 임베딩 생성
        text = f"{notice.title}. {notice.content}"
        embedding = embedding_service.get_embedding(text)
        notice.embedding = embedding
    
    db.commit()
    logger.info(f"✓ 공지사항 {len(notices)}개 임베딩 생성 완료")


def generate_embeddings_for_programs(db: Session, embedding_service):
    """지원 프로그램 임베딩 생성"""
    logger.info("지원 프로그램 임베딩 생성 중...")
    programs = db.query(SupportProgram).filter(SupportProgram.embedding == None).all()
    
    for program in programs:
        # 이름 + 설명을 합쳐서 임베딩 생성
        text = f"{program.name}. {program.description or ''}"
        embedding = embedding_service.get_embedding(text)
        program.embedding = embedding
    
    db.commit()
    logger.info(f"✓ 지원 프로그램 {len(programs)}개 임베딩 생성 완료")


def generate_embeddings_for_glossary(db: Session, embedding_service):
    """학사 용어 임베딩 생성"""
    logger.info("학사 용어 임베딩 생성 중...")
    glossary = db.query(AcademicGlossary).filter(AcademicGlossary.embedding == None).all()
    
    for term in glossary:
        # 용어 + 정의를 합쳐서 임베딩 생성
        text = f"{term.term_ko}. {term.definition}"
        embedding = embedding_service.get_embedding(text)
        term.embedding = embedding
    
    db.commit()
    logger.info(f"✓ 학사 용어 {len(glossary)}개 임베딩 생성 완료")


def main():
    """메인 함수"""
    logger.info("=" * 50)
    logger.info("임베딩 생성 시작")
    logger.info("=" * 50)
    
    # 데이터베이스 세션 및 임베딩 서비스
    db = SessionLocal()
    embedding_service = get_embedding_service()
    
    try:
        # 각 테이블의 데이터에 대해 임베딩 생성
        generate_embeddings_for_schedules(db, embedding_service)
        generate_embeddings_for_notices(db, embedding_service)
        generate_embeddings_for_programs(db, embedding_service)
        generate_embeddings_for_glossary(db, embedding_service)
        
        logger.info("=" * 50)
        logger.info("✓ 모든 임베딩 생성 완료!")
        logger.info("=" * 50)
        
    except Exception as e:
        logger.error(f"✗ 오류 발생: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()

"""Add performance indexes

Revision ID: 002_add_indexes
Revises: 001_add_embeddings
Create Date: 2026-01-22

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '002_add_indexes'
down_revision = '001_add_embeddings'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """성능 최적화를 위한 인덱스 추가"""
    
    # academic_schedules 테이블 인덱스
    op.create_index('ix_academic_schedules_category', 'academic_schedules', ['category'])
    op.create_index('ix_academic_schedules_dates', 'academic_schedules', ['start_date', 'end_date'])
    
    # notices 테이블 인덱스
    op.create_index('ix_notices_category', 'notices', ['category'])
    op.create_index('ix_notices_importance', 'notices', ['importance'])
    op.create_index('ix_notices_posted_date', 'notices', ['posted_date'])
    op.create_index('ix_notices_category_date', 'notices', ['category', 'posted_date'])
    
    # support_programs 테이블 인덱스
    op.create_index('ix_support_programs_category', 'support_programs', ['category'])
    op.create_index('ix_support_programs_application', 'support_programs', ['application_start', 'application_end'])
    op.create_index('ix_support_programs_status', 'support_programs', ['status'])
    
    # academic_glossary 테이블 인덱스
    op.create_index('ix_academic_glossary_category', 'academic_glossary', ['category'])
    op.create_index('ix_academic_glossary_term_ko', 'academic_glossary', ['term_ko'])
    
    # question_logs 테이블 인덱스 (질문 로그 분석용)
    # question_logs 테이블이 존재한다고 가정
    try:
        op.create_index('ix_question_logs_created_at', 'question_logs', ['created_at'])
        op.create_index('ix_question_logs_category', 'question_logs', ['category'])
    except Exception:
        # 테이블이 없으면 스킵
        pass


def downgrade() -> None:
    """인덱스 제거"""
    
    # question_logs 인덱스 제거
    try:
        op.drop_index('ix_question_logs_category', 'question_logs')
        op.drop_index('ix_question_logs_created_at', 'question_logs')
    except Exception:
        pass
    
    # academic_glossary 인덱스 제거
    op.drop_index('ix_academic_glossary_term_ko', 'academic_glossary')
    op.drop_index('ix_academic_glossary_category', 'academic_glossary')
    
    # support_programs 인덱스 제거
    op.drop_index('ix_support_programs_status', 'support_programs')
    op.drop_index('ix_support_programs_application', 'support_programs')
    op.drop_index('ix_support_programs_category', 'support_programs')
    
    # notices 인덱스 제거
    op.drop_index('ix_notices_category_date', 'notices')
    op.drop_index('ix_notices_posted_date', 'notices')
    op.drop_index('ix_notices_importance', 'notices')
    op.drop_index('ix_notices_category', 'notices')
    
    # academic_schedules 인덱스 제거
    op.drop_index('ix_academic_schedules_dates', 'academic_schedules')
    op.drop_index('ix_academic_schedules_category', 'academic_schedules')

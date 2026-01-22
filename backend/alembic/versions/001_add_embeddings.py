"""Add embedding columns and glossary table

Revision ID: 001_add_embeddings
Revises: 
Create Date: 2026-01-22

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from pgvector.sqlalchemy import Vector

# revision identifiers, used by Alembic.
revision = '001_add_embeddings'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 데이터베이스 타입 확인
    bind = op.get_bind()
    is_postgresql = bind.dialect.name == 'postgresql'
    
    if is_postgresql:
        # PostgreSQL에서만 pgvector 확장 설치
        op.execute('CREATE EXTENSION IF NOT EXISTS vector')
    
    # academic_schedules 테이블에 embedding 컬럼 추가
    # SQLite는 Vector 타입을 TEXT로 저장
    if is_postgresql:
        op.add_column('academic_schedules', sa.Column('embedding', Vector(384), nullable=True, comment='벡터 임베딩 (384차원)'))
        op.create_index('ix_academic_schedules_embedding', 'academic_schedules', ['embedding'], postgresql_using='ivfflat', postgresql_ops={'embedding': 'vector_cosine_ops'})
    else:
        op.add_column('academic_schedules', sa.Column('embedding', sa.Text(), nullable=True))
    
    # notices 테이블에 embedding 컬럼 추가
    if is_postgresql:
        op.add_column('notices', sa.Column('embedding', Vector(384), nullable=True, comment='벡터 임베딩 (384차원)'))
        op.create_index('ix_notices_embedding', 'notices', ['embedding'], postgresql_using='ivfflat', postgresql_ops={'embedding': 'vector_cosine_ops'})
    else:
        op.add_column('notices', sa.Column('embedding', sa.Text(), nullable=True))
    
    # support_programs 테이블에 embedding 컬럼 추가
    if is_postgresql:
        op.add_column('support_programs', sa.Column('embedding', Vector(384), nullable=True, comment='벡터 임베딩 (384차원)'))
        op.create_index('ix_support_programs_embedding', 'support_programs', ['embedding'], postgresql_using='ivfflat', postgresql_ops={'embedding': 'vector_cosine_ops'})
    else:
        op.add_column('support_programs', sa.Column('embedding', sa.Text(), nullable=True))
    
    # academic_glossary 테이블 생성
    if is_postgresql:
        op.create_table(
            'academic_glossary',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('term_ko', sa.String(200), nullable=False, comment='한국어 용어'),
            sa.Column('term_en', sa.String(200), nullable=True, comment='영문 용어'),
            sa.Column('definition', sa.Text(), nullable=False, comment='정의 및 설명'),
            sa.Column('examples', sa.Text(), nullable=True, comment='예시'),
            sa.Column('category', sa.String(100), nullable=True, comment='카테고리'),
            sa.Column('embedding', Vector(384), nullable=True, comment='벡터 임베딩 (384차원)'),
            sa.Column('created_at', sa.Date(), nullable=False, comment='생성일'),
            sa.Column('updated_at', sa.Date(), nullable=True, comment='수정일'),
            sa.PrimaryKeyConstraint('id')
        )
        op.create_index('ix_academic_glossary_id', 'academic_glossary', ['id'])
        op.create_index('ix_academic_glossary_embedding', 'academic_glossary', ['embedding'], postgresql_using='ivfflat', postgresql_ops={'embedding': 'vector_cosine_ops'})
    else:
        op.create_table(
            'academic_glossary',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('term_ko', sa.String(200), nullable=False),
            sa.Column('term_en', sa.String(200), nullable=True),
            sa.Column('definition', sa.Text(), nullable=False),
            sa.Column('examples', sa.Text(), nullable=True),
            sa.Column('category', sa.String(100), nullable=True),
            sa.Column('embedding', sa.Text(), nullable=True),
            sa.Column('created_at', sa.Date(), nullable=False),
            sa.Column('updated_at', sa.Date(), nullable=True),
            sa.PrimaryKeyConstraint('id')
        )
        op.create_index('ix_academic_glossary_id', 'academic_glossary', ['id'])


def downgrade() -> None:
    # 데이터베이스 타입 확인
    bind = op.get_bind()
    is_postgresql = bind.dialect.name == 'postgresql'
    
    # academic_glossary 테이블 삭제
    if is_postgresql:
        op.drop_index('ix_academic_glossary_embedding', 'academic_glossary')
    op.drop_index('ix_academic_glossary_id', 'academic_glossary')
    op.drop_table('academic_glossary')
    
    # embedding 컬럼 제거
    if is_postgresql:
        op.drop_index('ix_support_programs_embedding', 'support_programs')
    op.drop_column('support_programs', 'embedding')
    
    if is_postgresql:
        op.drop_index('ix_notices_embedding', 'notices')
    op.drop_column('notices', 'embedding')
    
    if is_postgresql:
        op.drop_index('ix_academic_schedules_embedding', 'academic_schedules')
    op.drop_column('academic_schedules', 'embedding')
    
    # pgvector 확장 제거 (주의: 다른 곳에서 사용 중이면 제거하지 말것)
    # op.execute('DROP EXTENSION IF EXISTS vector')

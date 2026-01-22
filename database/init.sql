# PostgreSQL 초기화 스크립트

-- pgvector 확장 생성 (이미 생성되어 있을 수 있음)
CREATE EXTENSION IF NOT EXISTS vector;

-- 한국어 로케일 설정 확인
SHOW lc_collate;
SHOW lc_ctype;

-- 데이터베이스 정보 출력
SELECT version();

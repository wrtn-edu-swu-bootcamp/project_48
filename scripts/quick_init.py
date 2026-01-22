"""
데이터베이스 초기화 및 시드 데이터 입력
"""
import sys
import os
from pathlib import Path

# 프로젝트 루트 경로 설정
project_root = Path(__file__).parent.parent
backend_path = project_root / "backend"
sys.path.insert(0, str(backend_path))

# 백엔드 모듈 임포트
os.chdir(str(backend_path))

from app.core.database import engine, Base
from app.models import *

def init_database():
    """데이터베이스 테이블 생성"""
    print("=" * 60)
    print("데이터베이스 초기화 시작")
    print("=" * 60)
    
    try:
        # 모든 테이블 생성
        Base.metadata.create_all(bind=engine)
        print("✓ 데이터베이스 테이블 생성 완료")
        print("=" * 60)
        
    except Exception as e:
        print(f"✗ 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    init_database()

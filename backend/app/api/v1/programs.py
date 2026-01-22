"""
지원 프로그램 API 엔드포인트
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.support_program import SupportProgram
from app.schemas.support_program import SupportProgramResponse

router = APIRouter()


@router.get("/api/v1/programs", response_model=List[SupportProgramResponse])
async def get_programs(
    program_type: str = None,
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db),
):
    """
    지원 프로그램 조회 엔드포인트

    쿼리 파라미터:
    - program_type: 프로그램 유형 필터 (예: "장학금", "비교과 프로그램")
    - limit: 최대 결과 수 (기본값: 20)
    - offset: 건너뛸 결과 수 (기본값: 0)
    """
    try:
        query = db.query(SupportProgram)

        if program_type:
            query = query.filter(SupportProgram.program_type == program_type)

        programs = query.order_by(SupportProgram.created_at.desc()).offset(offset).limit(limit).all()

        return programs

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/api/v1/programs/{program_id}", response_model=SupportProgramResponse)
async def get_program(
    program_id: int,
    db: Session = Depends(get_db),
):
    """
    특정 지원 프로그램 조회 엔드포인트
    """
    try:
        program = db.query(SupportProgram).filter(SupportProgram.id == program_id).first()

        if not program:
            raise HTTPException(status_code=404, detail="프로그램을 찾을 수 없습니다")

        return program

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
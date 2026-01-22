"""
학사 일정 API 엔드포인트
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.academic_schedule import AcademicSchedule
from app.schemas.academic_schedule import AcademicScheduleResponse
from datetime import datetime

router = APIRouter()


@router.get("/schedules", response_model=List[AcademicScheduleResponse])
async def get_schedules(
    semester: str = None,
    schedule_type: str = None,
    db: Session = Depends(get_db),
):
    """
    학사 일정 조회 엔드포인트

    쿼리 파라미터:
    - semester: 학기 필터 (예: "1학기", "2학기")
    - schedule_type: 일정 유형 필터 (예: "수강신청", "등록금 납부")
    """
    try:
        query = db.query(AcademicSchedule)

        if semester:
            query = query.filter(AcademicSchedule.semester == semester)

        if schedule_type:
            query = query.filter(AcademicSchedule.schedule_type == schedule_type)

        # 현재 날짜 이후의 일정만 조회
        query = query.filter(AcademicSchedule.start_date >= datetime.now().date())

        schedules = query.order_by(AcademicSchedule.start_date).all()

        return schedules

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/api/v1/schedules/{schedule_id}", response_model=AcademicScheduleResponse)
async def get_schedule(
    schedule_id: int,
    db: Session = Depends(get_db),
):
    """
    특정 학사 일정 조회 엔드포인트
    """
    try:
        schedule = db.query(AcademicSchedule).filter(
            AcademicSchedule.id == schedule_id
        ).first()

        if not schedule:
            raise HTTPException(status_code=404, detail="일정을 찾을 수 없습니다")

        return schedule

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
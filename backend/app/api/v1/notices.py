"""
공지사항 API 엔드포인트
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.notice import Notice
from app.schemas.notice import NoticeResponse

router = APIRouter()


@router.get("/api/v1/notices", response_model=List[NoticeResponse])
async def get_notices(
    category: str = None,
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db),
):
    """
    공지사항 조회 엔드포인트

    쿼리 파라미터:
    - category: 카테고리 필터
    - limit: 최대 결과 수 (기본값: 20)
    - offset: 건너뛸 결과 수 (기본값: 0)
    """
    try:
        query = db.query(Notice)

        if category:
            query = query.filter(Notice.category == category)

        notices = query.order_by(Notice.created_at.desc()).offset(offset).limit(limit).all()

        return notices

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/api/v1/notices/{notice_id}", response_model=NoticeResponse)
async def get_notice(
    notice_id: int,
    db: Session = Depends(get_db),
):
    """
    특정 공지사항 조회 엔드포인트
    """
    try:
        notice = db.query(Notice).filter(Notice.id == notice_id).first()

        if not notice:
            raise HTTPException(status_code=404, detail="공지사항을 찾을 수 없습니다")

        return notice

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
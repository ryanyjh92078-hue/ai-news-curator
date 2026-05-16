from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Keyword

router = APIRouter()


@router.get("/keywords/trending")
def get_trending_keywords(
    limit: int = Query(20, ge=1, le=50),
    db: Session = Depends(get_db),
):
    keywords = (
        db.query(Keyword)
        .order_by(Keyword.trend_score.desc())
        .limit(limit)
        .all()
    )
    return keywords


@router.get("/keywords")
def get_all_keywords(db: Session = Depends(get_db)):
    return db.query(Keyword).order_by(Keyword.count.desc()).all()

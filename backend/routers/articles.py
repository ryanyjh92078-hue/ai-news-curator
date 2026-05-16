from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from ..database import get_db
from ..models import Article

router = APIRouter()


@router.get("/articles")
def get_articles(
    keyword: Optional[str] = Query(None, description="필터링할 키워드"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    q = db.query(Article)
    if keyword:
        q = q.filter(
            (Article.title.ilike(f"%{keyword}%")) |
            (Article.content.ilike(f"%{keyword}%"))
        )
    total = q.count()
    items = q.order_by(Article.published_at.desc()).offset(offset).limit(limit).all()
    return {"total": total, "items": items}


@router.get("/articles/{article_id}")
def get_article(article_id: int, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="기사를 찾을 수 없습니다.")
    return article

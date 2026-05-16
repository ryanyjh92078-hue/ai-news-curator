from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from ..database import get_db
from ..models import Summary, Article
from ..ai.gemini_client import gemini_summarize

router = APIRouter()


class SummaryRequest(BaseModel):
    keyword: str


@router.post("/summaries/generate")
async def generate_summary(req: SummaryRequest, db: Session = Depends(get_db)):
    keyword = req.keyword.strip()

    # 최근 24시간 내 동일 키워드 요약이 있으면 재사용
    from datetime import datetime, timedelta
    recent = (
        db.query(Summary)
        .filter(Summary.keyword == keyword)
        .filter(Summary.created_at >= datetime.utcnow() - timedelta(hours=24))
        .order_by(Summary.created_at.desc())
        .first()
    )
    if recent:
        return {"keyword": keyword, "summary": recent.content, "cached": True}

    # 관련 기사 조회
    articles = (
        db.query(Article)
        .filter(
            (Article.title.ilike(f"%{keyword}%")) |
            (Article.content.ilike(f"%{keyword}%"))
        )
        .order_by(Article.published_at.desc())
        .limit(10)
        .all()
    )

    if not articles:
        raise HTTPException(status_code=404, detail="관련 기사가 없습니다.")

    # Gemini로 심층 요약 생성
    summary_text = await gemini_summarize(keyword, articles)

    # DB 저장
    summary = Summary(
        keyword=keyword,
        content=summary_text,
        article_count=len(articles),
    )
    db.add(summary)
    db.commit()

    return {"keyword": keyword, "summary": summary_text, "cached": False}


@router.get("/summaries/{keyword}")
def get_summary(keyword: str, db: Session = Depends(get_db)):
    summary = (
        db.query(Summary)
        .filter(Summary.keyword == keyword)
        .order_by(Summary.created_at.desc())
        .first()
    )
    if not summary:
        raise HTTPException(status_code=404, detail="요약이 없습니다. /generate를 먼저 호출하세요.")
    return summary

"""
Render Cron Job 진입점
스케줄: 매 6시간마다 (render.yaml에서 설정)
실행 명령: python -m backend.crawler.run
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from datetime import datetime
from backend.crawler.fetcher import fetch_news
from backend.crawler.keyword_extractor import extract_keywords
from backend.database import SessionLocal
from backend.models import Article, Keyword


def save_articles(articles: list[dict], db) -> int:
    saved = 0
    for item in articles:
        exists = db.query(Article).filter(Article.url == item["url"]).first()
        if exists:
            continue
        article = Article(**item)
        db.add(article)
        saved += 1
    db.commit()
    return saved


def update_keywords(keyword_counts: list[tuple], db):
    for word, count in keyword_counts:
        existing = db.query(Keyword).filter(Keyword.word == word).first()
        if existing:
            existing.count += count
            existing.trend_score = min(existing.count, 1000)
        else:
            kw = Keyword(word=word, count=count, trend_score=count)
            db.add(kw)
    db.commit()


def run():
    print(f"[{datetime.utcnow()}] 크롤러 시작")
    db = SessionLocal()

    try:
        # 1. 뉴스 수집
        articles = fetch_news()

        # 2. DB 저장
        saved_count = save_articles(articles, db)
        print(f"[crawler] 신규 기사 {saved_count}건 저장")

        # 3. 키워드 추출
        keyword_counts = extract_keywords(articles)
        print(f"[crawler] 키워드 {len(keyword_counts)}개 추출")

        # 4. 키워드 업데이트
        update_keywords(keyword_counts, db)
        print(f"[crawler] 키워드 DB 업데이트 완료")

    except Exception as e:
        print(f"[crawler] 오류 발생: {e}")
        raise
    finally:
        db.close()

    print(f"[{datetime.utcnow()}] 크롤러 완료")


if __name__ == "__main__":
    run()

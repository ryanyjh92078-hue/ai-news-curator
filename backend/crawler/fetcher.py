import os
import httpx
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
NEWS_API_URL = "https://newsapi.org/v2/everything"

QUERIES = [
    "LLM large language model",
    "AI machine learning research",
    "software engineering developer tools",
    "open source AI framework",
    "GPU computing inference",
]


def fetch_news() -> list[dict]:
    all_articles = []
    seen_urls = set()

    with httpx.Client(timeout=15) as client:
        for query in QUERIES:
            try:
                resp = client.get(NEWS_API_URL, params={
                    "q": query,
                    "language": "en",
                    "sortBy": "publishedAt",
                    "pageSize": 20,
                    "apiKey": NEWS_API_KEY,
                })
                resp.raise_for_status()
                data = resp.json()

                for item in data.get("articles", []):
                    url = item.get("url", "")
                    if url in seen_urls or not url:
                        continue
                    seen_urls.add(url)

                    published = item.get("publishedAt", "")
                    try:
                        published_dt = datetime.fromisoformat(published.replace("Z", "+00:00"))
                    except Exception:
                        published_dt = datetime.utcnow()

                    all_articles.append({
                        "title": item.get("title", "")[:500],
                        "content": (item.get("content") or item.get("description") or "")[:2000],
                        "url": url[:1000],
                        "source": item.get("source", {}).get("name", "")[:100],
                        "published_at": published_dt,
                    })

            except Exception as e:
                print(f"[fetcher] 쿼리 '{query}' 오류: {e}")

    print(f"[fetcher] 총 {len(all_articles)}건 수집 완료")
    return all_articles

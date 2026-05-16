from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routers import articles, keywords, summaries

# 테이블 자동 생성 (Neon DB에 테이블이 없으면 만들어줌)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI News Curator API",
    description="정보과학 전문가를 위한 지능형 뉴스 큐레이션 시스템",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(articles.router, prefix="/api", tags=["articles"])
app.include_router(keywords.router, prefix="/api", tags=["keywords"])
app.include_router(summaries.router, prefix="/api", tags=["summaries"])


@app.get("/")
def root():
    return {"status": "ok", "message": "AI News Curator API"}


@app.get("/health")
def health():
    return {"status": "healthy"}

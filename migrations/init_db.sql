-- Neon 콘솔 SQL Editor에서 처음 한 번만 실행하세요.
-- SQLAlchemy가 자동으로 테이블을 만들어주므로 생략 가능하지만,
-- 인덱스 최적화를 위해 직접 실행 권장.

CREATE TABLE IF NOT EXISTS articles (
    id          SERIAL PRIMARY KEY,
    title       VARCHAR(500)  NOT NULL,
    content     TEXT,
    url         VARCHAR(1000) NOT NULL UNIQUE,
    source      VARCHAR(100),
    published_at TIMESTAMP,
    created_at  TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS keywords (
    id          SERIAL PRIMARY KEY,
    word        VARCHAR(100)  NOT NULL UNIQUE,
    count       INTEGER       DEFAULT 0,
    trend_score INTEGER       DEFAULT 0,
    updated_at  TIMESTAMP     DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS summaries (
    id            SERIAL PRIMARY KEY,
    keyword       VARCHAR(100) NOT NULL,
    content       TEXT         NOT NULL,
    article_count INTEGER      DEFAULT 0,
    created_at    TIMESTAMP    DEFAULT NOW()
);

-- 인덱스
CREATE INDEX IF NOT EXISTS idx_articles_published  ON articles(published_at DESC);
CREATE INDEX IF NOT EXISTS idx_articles_title      ON articles USING gin(to_tsvector('english', title));
CREATE INDEX IF NOT EXISTS idx_keywords_trend      ON keywords(trend_score DESC);
CREATE INDEX IF NOT EXISTS idx_summaries_keyword   ON summaries(keyword);
CREATE INDEX IF NOT EXISTS idx_summaries_created   ON summaries(created_at DESC);

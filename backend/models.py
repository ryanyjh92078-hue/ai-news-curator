from sqlalchemy import Column, Integer, String, Text, DateTime, func
from .database import Base


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False)
    content = Column(Text)
    url = Column(String(1000), unique=True, nullable=False)
    source = Column(String(100))
    published_at = Column(DateTime)
    created_at = Column(DateTime, server_default=func.now())


class Keyword(Base):
    __tablename__ = "keywords"

    id = Column(Integer, primary_key=True, index=True)
    word = Column(String(100), unique=True, nullable=False)
    count = Column(Integer, default=0)
    trend_score = Column(Integer, default=0)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class Summary(Base):
    __tablename__ = "summaries"

    id = Column(Integer, primary_key=True, index=True)
    keyword = Column(String(100), nullable=False, index=True)
    content = Column(Text, nullable=False)
    article_count = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())

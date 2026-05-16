# AI News Curator
정보과학 전문가를 위한 지능형 뉴스 큐레이션 및 심층 요약 시스템

## 기술 스택
- **Backend**: FastAPI + SQLAlchemy
- **Database**: Neon (서버리스 PostgreSQL)
- **AI**: Google Gemini 1.5 Pro
- **Hosting**: Render (Web Service + Cron Job + Static Site)

## 로컬 설치

```bash
git clone https://github.com/yourname/ai-news-curator
cd ai-news-curator
pip install -r requirements.txt
cp .env.example .env   # 값 직접 채우기
python -m backend.main
```

## 환경변수 설정

| 변수명 | 설명 | 발급 위치 |
|--------|------|-----------|
| `DATABASE_URL` | Neon PostgreSQL 연결 문자열 | Neon 콘솔 → Connection string |
| `GEMINI_API_KEY` | Google Gemini API 키 | Google AI Studio |
| `NEWS_API_KEY` | 뉴스 수집 API 키 | newsapi.org |
| `SECRET_KEY` | JWT 서명용 임의 문자열 | 직접 생성 |

## 배포 순서

1. **Neon**: 프로젝트 생성 → `migrations/init_db.sql` 실행
2. **GitHub**: 이 레포 push
3. **Render**: GitHub 연결 → `render.yaml` 자동 감지 → 환경변수 입력

## API 엔드포인트

| Method | Path | 설명 |
|--------|------|------|
| GET | `/api/articles` | 뉴스 목록 조회 (keyword 필터 가능) |
| GET | `/api/keywords/trending` | 트렌드 키워드 상위 20개 |
| POST | `/api/summaries/generate` | 키워드 기반 AI 심층 요약 생성 |
| GET | `/api/summaries/{keyword}` | 기존 요약 조회 |

import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

SYSTEM_PROMPT = """당신은 정보과학 및 AI 분야의 시니어 리서처입니다.
주어진 뉴스 기사들을 분석하여 다음 구조로 심층 요약을 작성하세요.

[요약 구조]
1. 핵심 동향 (2~3문장): 이 키워드와 관련해 지금 무슨 일이 일어나고 있는가
2. 기술적 맥락: 어떤 기술적 원리나 구현 방식이 핵심인가
3. 산업적 의의: 왜 중요한가, 어떤 영향을 미치는가
4. 주목할 포인트: 개발자/연구자가 특히 주시해야 할 부분

조건:
- 전문 용어는 유지하되 인과관계를 명확히 설명
- 총 400~600자 분량
- 한국어로 작성
"""


async def gemini_summarize(keyword: str, articles: list) -> str:
    # 기사 컨텍스트 구성
    context = "\n\n".join([
        f"제목: {a.title}\n내용: {(a.content or '')[:400]}"
        for a in articles
    ])

    prompt = f"{SYSTEM_PROMPT}\n\n[키워드]\n{keyword}\n\n[관련 뉴스 {len(articles)}건]\n{context}"

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        raise RuntimeError(f"Gemini API 오류: {str(e)}")

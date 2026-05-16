import re
from collections import Counter

# 기술 분야에서 의미 없는 일반 단어 제거
STOPWORDS = {
    "the", "and", "for", "with", "this", "that", "are", "from",
    "have", "been", "will", "can", "new", "more", "also", "its",
    "has", "was", "not", "but", "they", "their", "how", "what",
    "when", "which", "about", "into", "than", "said", "says",
    "model", "system", "data", "using", "based", "team", "company",
    "week", "year", "time", "way", "make", "use", "help",
}

# 알려진 기술 키워드에 가중치 부여
TECH_BOOST = {
    "llm", "gpt", "transformer", "inference", "rag", "finetune",
    "cuda", "pytorch", "tensorflow", "kubernetes", "docker",
    "agent", "embedding", "vector", "diffusion", "multimodal",
    "benchmark", "openai", "anthropic", "gemini", "mistral",
    "rust", "python", "typescript", "golang", "webassembly",
}


def extract_keywords(articles: list[dict]) -> list[tuple[str, int]]:
    word_counts: Counter = Counter()

    for article in articles:
        text = (article.get("title", "") + " " + article.get("content", ""))

        # 대문자로 시작하거나 전부 대문자인 단어 (기술 용어, 고유명사)
        tech_words = re.findall(r'\b[A-Z][a-zA-Z]{2,}\b', text)
        # 소문자지만 기술 키워드인 단어
        lower_words = re.findall(r'\b[a-z]{3,}\b', text.lower())

        for w in tech_words:
            clean = w.strip()
            if clean.lower() not in STOPWORDS and len(clean) > 2:
                score = 3 if clean.lower() in TECH_BOOST else 1
                word_counts[clean] += score

        for w in lower_words:
            if w in TECH_BOOST:
                word_counts[w.upper()] += 2

    # 상위 30개 반환
    return word_counts.most_common(30)

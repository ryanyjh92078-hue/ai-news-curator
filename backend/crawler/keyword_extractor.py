import re
from collections import Counter

STOPWORDS = {
    # 일반 영어 단어
    "the", "and", "for", "with", "this", "that", "are", "from",
    "have", "been", "will", "can", "new", "more", "also", "its",
    "has", "was", "not", "but", "they", "their", "how", "what",
    "when", "which", "about", "into", "than", "said", "says",
    "use", "help", "make", "way", "time", "year", "week",
    # 노이즈 단어
    "May", "Why", "Inc", "Ping", "India", "Just", "Here", "Like",
    "Get", "One", "Two", "Now", "See", "Top", "Big", "Our", "Your",
    "Artificial", "Intelligence", "Could", "Would", "Should",
    "Every", "After", "Before", "While", "Where", "There",
    "These", "Those", "Been", "Does", "Did", "Had", "Has",
    "Without", "Within", "Through", "During", "Between",
    "According", "Including", "However", "Although", "Because",
    # 날짜/숫자 관련
    "January", "February", "March", "April", "June", "July",
    "August", "September", "October", "November", "December",
    "Monday", "Tuesday", "Wednesday", "Thursday", "Friday",
    "Saturday", "Sunday",
}

# 핵심 기술 키워드 가중치
TECH_BOOST = {
    "llm", "gpt", "transformer", "inference", "rag", "finetune",
    "cuda", "pytorch", "tensorflow", "kubernetes", "docker",
    "agent", "embedding", "vector", "diffusion", "multimodal",
    "benchmark", "openai", "anthropic", "gemini", "mistral",
    "rust", "python", "typescript", "golang", "webassembly",
    "claude", "deepseek", "llama", "groq", "nvidia", "amd",
    "copilot", "cursor", "langchain", "huggingface",
}


def extract_keywords(articles: list[dict]) -> list[tuple[str, int]]:
    word_counts: Counter = Counter()

    for article in articles:
        text = (article.get("title", "") + " " + article.get("content", ""))

        # 대문자로 시작하는 단어 (기술 용어, 고유명사)
        tech_words = re.findall(r'\b[A-Z][a-zA-Z]{3,}\b', text)
        # 소문자 기술 키워드
        lower_words = re.findall(r'\b[a-z]{3,}\b', text.lower())

        for w in tech_words:
            clean = w.strip()
            if clean not in STOPWORDS and clean.lower() not in STOPWORDS:
                score = 3 if clean.lower() in TECH_BOOST else 1
                word_counts[clean] += score

        for w in lower_words:
            if w in TECH_BOOST:
                word_counts[w.upper()] += 2

    return word_counts.most_common(30)

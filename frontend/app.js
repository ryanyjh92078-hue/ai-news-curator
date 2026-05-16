// Render에 배포된 백엔드 API 주소 (배포 후 실제 주소로 변경)
const API = "https://ai-news-curator-qstb.onrender.com/api";

let activeKeyword = null;

// ── 초기화 ──────────────────────────────────────────
document.addEventListener("DOMContentLoaded", () => {
  loadKeywords();
});

// ── 트렌드 키워드 로드 ──────────────────────────────
async function loadKeywords() {
  const container = document.getElementById("keywords-container");
  try {
    const res = await fetch(`${API}/keywords/trending?limit=25`);
    if (!res.ok) throw new Error(res.statusText);
    const keywords = await res.json();

    if (keywords.length === 0) {
      container.innerHTML = '<span class="loading">수집된 키워드가 없습니다. 잠시 후 다시 시도하세요.</span>';
      return;
    }

    container.innerHTML = keywords
      .map(k => `<button class="keyword-tag" onclick="onKeywordClick('${k.word}')">${k.word}</button>`)
      .join("");
  } catch (e) {
    container.innerHTML = `<span class="error">키워드를 불러오지 못했습니다: ${e.message}</span>`;
  }
}

// ── 키워드 클릭 ─────────────────────────────────────
async function onKeywordClick(keyword) {
  // 이전 active 해제
  document.querySelectorAll(".keyword-tag").forEach(el => el.classList.remove("active"));
  const clicked = [...document.querySelectorAll(".keyword-tag")].find(el => el.textContent === keyword);
  if (clicked) clicked.classList.add("active");

  activeKeyword = keyword;

  // 요약 패널 열기
  const summarySection = document.getElementById("summary-section");
  summarySection.classList.remove("hidden");
  document.getElementById("summary-keyword").textContent = keyword;
  document.getElementById("summary-content").innerHTML = '<div class="loading">Gemini가 분석 중입니다...</div>';

  // 관련 기사 로드 & 요약 생성 동시 실행
  await Promise.all([
    generateSummary(keyword),
    loadArticles(keyword),
  ]);
}

// ── AI 심층 요약 생성 ────────────────────────────────
async function generateSummary(keyword) {
  const content = document.getElementById("summary-content");
  try {
    const res = await fetch(`${API}/summaries/generate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ keyword }),
    });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || res.statusText);
    }
    const data = await res.json();
    content.textContent = data.summary;
    if (data.cached) {
      content.insertAdjacentHTML("afterbegin", '<span style="font-size:11px;color:#475569;display:block;margin-bottom:8px">캐시된 요약 (24시간 이내)</span>');
    }
  } catch (e) {
    content.innerHTML = `<span class="error">요약 생성 실패: ${e.message}</span>`;
  }
}

// ── 관련 뉴스 로드 ───────────────────────────────────
async function loadArticles(keyword) {
  const section = document.getElementById("articles-section");
  const container = document.getElementById("articles-container");
  section.classList.remove("hidden");
  container.innerHTML = '<div class="loading">기사 로딩 중...</div>';

  try {
    const res = await fetch(`${API}/articles?keyword=${encodeURIComponent(keyword)}&limit=8`);
    if (!res.ok) throw new Error(res.statusText);
    const data = await res.json();

    if (data.items.length === 0) {
      container.innerHTML = '<div class="loading">관련 기사가 없습니다.</div>';
      return;
    }

    container.innerHTML = data.items.map(a => `
      <div class="article-card">
        <a class="article-title" href="${a.url}" target="_blank" rel="noopener">${a.title}</a>
        <div class="article-meta">
          <span>${a.source || "Unknown"}</span>
          <span>${formatDate(a.published_at)}</span>
        </div>
      </div>
    `).join("");
  } catch (e) {
    container.innerHTML = `<span class="error">기사를 불러오지 못했습니다: ${e.message}</span>`;
  }
}

// ── 요약 패널 닫기 ───────────────────────────────────
function closeSummary() {
  document.getElementById("summary-section").classList.add("hidden");
  document.getElementById("articles-section").classList.add("hidden");
  document.querySelectorAll(".keyword-tag").forEach(el => el.classList.remove("active"));
  activeKeyword = null;
}

// ── 유틸: 날짜 포맷 ─────────────────────────────────
function formatDate(dateStr) {
  if (!dateStr) return "";
  const d = new Date(dateStr);
  return d.toLocaleDateString("ko-KR", { month: "short", day: "numeric" });
}

# core/handler.py
import logging
import asyncio
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import lru_cache
from .search import ddg_search
from .fetcher import fetch_page_text
from .rerank import rerank_snippets
from .summarize import summarize
from config import MAX_PAGES, MAX_CHARS, MAX_WORKERS, NUM_SEARCH_RESULTS

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# ------------------------------
# ⚡ Optimizations applied:
# - Caching search results & summaries (lru_cache)
# - Async + ThreadPool mix for concurrent fetch
# - Truncate text early to avoid large summarization load
# - Graceful degradation (fallbacks)
# - Reduced I/O waits and reused threads
# ------------------------------

# ✅ Cache search results (avoid re-hitting DuckDuckGo)
@lru_cache(maxsize=32)
def cached_search(query):
    return ddg_search(query, top_k=NUM_SEARCH_RESULTS)

# ✅ Concurrently fetch pages with timeout and fewer workers for better CPU usage
def _fetch_pages(results, max_pages=MAX_PAGES, timeout=10, max_workers=MAX_WORKERS):
    pages = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_meta = {executor.submit(fetch_page_text, r["link"]): r for r in results[:max_pages]}
        for fut in as_completed(future_to_meta):
            meta = future_to_meta[fut]
            try:
                text = fut.result(timeout=timeout)
                pages.append({
                    "title": meta.get("title", ""),
                    "link": meta.get("link", ""),
                    "snippet": meta.get("snippet", ""),
                    "text": text
                })
            except Exception as e:
                logging.warning("⚠️ Error fetching page: %s", e)
    return pages

# ✅ Cache summaries to avoid recomputation
@lru_cache(maxsize=64)
def cached_summary(text):
    try:
        return summarize(text).strip()
    except Exception as e:
        logging.warning(f"Summarization failed: {e}")
        return ""

# ✅ Main handler (optimized)
def handler(query, top_k=3):
    """
    Efficient web search + summarization handler.
    Returns:
    {
      "answer": "Readable formatted answer in bullets with links",
      "sources": [{"title":..., "link":...}],
      "meta": {...}
    }
    """
    if not query or len(query.strip()) == 0:
        return {"answer": "Please enter a valid query.", "sources": [], "meta": {}}

    # 1️⃣ Cached Search
    results = cached_search(query)
    if not results:
        return {"answer": "No search results found.", "sources": [], "meta": {}}

    # 2️⃣ Prepare snippets for reranking
    snippets = [
        {
            "text": (r.get("snippet", "") + " " + r.get("title", "")),
            "link": r["link"],
            "title": r.get("title", "")
        }
        for r in results
    ]

    # 3️⃣ Lightweight Reranking (top_k only)
    ranked = rerank_snippets(query, snippets, top_k=top_k)

    # 4️⃣ Concurrent Fetch (with timeout)
    pages = _fetch_pages(ranked, max_pages=top_k)

    # 5️⃣ Fast Summarization (truncate + cache)
    page_summaries = []
    for p in pages:
        text = (p.get("text", "") or "")[:3000]  # truncate long pages
        snippet_text = p.get("snippet", "")
        summary = ""

        if len(text) > 100:
            summary = cached_summary(text)
        elif snippet_text:
            summary = snippet_text

        if len(summary) > MAX_CHARS:
            summary = summary[:MAX_CHARS].rsplit('.', 1)[0] + "..."

        if summary:
            formatted = f"• {summary} ([{p['title']}]({p['link']}))"
            page_summaries.append(formatted)

    # 6️⃣ Final Formatting
    if not page_summaries:
        return {"answer": "No concise answer found.", "sources": [], "meta": {"results_count": len(results)}}

    final_answer = "\n\n".join(page_summaries)

    return {
        "answer": final_answer,
        "sources": [{"title": p["title"], "link": p["link"]} for p in pages],
        "meta": {"results_count": len(results)}
    }

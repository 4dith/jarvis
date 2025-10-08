# handler.py
from .search import ddg_search
from .fetcher import fetch_page_text
from .rerank import rerank_snippets
from .summarize import summarize
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from config import MAX_PAGES, MAX_CHARS, MAX_WORKERS, NUM_SEARCH_RESULTS

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def _fetch_pages(results, max_pages=MAX_PAGES, timeout=15, max_workers=MAX_WORKERS):
    """Fetch pages concurrently."""
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
                logging.exception("Error fetching page: %s", e)
    return pages

def handler(query, top_k=3):
    """
    Returns:
    {
      "answer": "Readable formatted answer in bullets with links",
      "sources": [{"title":..., "link":...}],
      "meta": {...}
    }
    """
    # 1) Search
    results = ddg_search(query, top_k=NUM_SEARCH_RESULTS)
    if not results:
        return {"answer": "No results found.", "sources": [], "meta": {}}

    # 2) Prepare snippets for reranking
    snippets = [{"text": (r.get("snippet","") + " " + r.get("title","")), "link": r["link"], "title": r.get("title","")} for r in results]

    # 3) Rerank
    ranked = rerank_snippets(query, snippets, top_k=top_k)

    # 4) Fetch pages
    pages = _fetch_pages(ranked, max_pages=top_k)

    # 5) Summarize and format
    page_summaries = []
    for p in pages:
        text = p.get("text", "")
        snippet_text = p.get("snippet", "")
        summary = ""
        if text and len(text) > 100:
            try:
                summary = summarize(text).strip()
            except:
                summary = snippet_text.strip()
        else:
            summary = snippet_text.strip()

        if len(summary) > MAX_CHARS:
            summary = summary[:MAX_CHARS].rsplit('.', 1)[0] + "..."

        if summary:
            page_summaries.append(f"• {summary} ([{p['title']}]({p['link']}))")

    if not page_summaries:
        return {"answer": "No concise answer found.", "sources": [], "meta": {"query_results_count": len(results)}}

    final_answer = "\n\n".join(page_summaries)

    return {
        "answer": final_answer,
        "sources": [{"title": p["title"], "link": p["link"]} for p in pages],
        "meta": {"query_results_count": len(results)}
    }

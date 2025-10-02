from .search import ddg_search
from .fetcher import fetch_page_text
from .rerank import rerank_snippets
from .summarize import summarize
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


def _fetch_pages(results, max_pages=3, timeout=15, max_workers=4):
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


def handler(query, top_k=3, max_chars=350):
    """
    Returns:
    {
      "answer": "Readable formatted answer in bullets with links",
      "sources": [{"title":..., "link":...}],
      "meta": {...}
    }
    """
    # 1) Search
    results = ddg_search(query, top_k=6)
    if not results:
        return {"answer": "No results found.", "sources": [], "meta": {}}

    # 2) Prepare snippets for reranking
    snippets = [{"text": (r.get("snippet","") + " " + r.get("title","")), "link": r["link"], "title": r.get("title","")} for r in results]

    # 3) Re-rank
    ranked = rerank_snippets(query, snippets, top_k=top_k)

    # 4) Fetch pages
    pages = _fetch_pages(ranked, max_pages=top_k)

    # 5) Summarize and format each page
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

        # Limit summary length
        if len(summary) > max_chars:
            summary = summary[:max_chars].rsplit('.', 1)[0] + "..."

        # Format bullet with link
        if summary:
            page_summaries.append(f"• {summary} ([{p['title']}]({p['link']}))")

    if not page_summaries:
        return {"answer": "No concise answer found.", "sources": [], "meta": {"query_results_count": len(results)}}

    # 6) Combine all summaries
    final_answer = "\n\n".join(page_summaries)

    return {
        "answer": final_answer,
        "sources": [{"title": p["title"], "link": p["link"]} for p in pages],
        "meta": {"query_results_count": len(results)}
    }

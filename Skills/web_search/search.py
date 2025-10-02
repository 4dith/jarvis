from ddgs import DDGS
import logging

def ddg_search(query, top_k=5):
    results = []
    try:
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=top_k):
                results.append({
                    "title": r.get("title", ""),
                    "link": r.get("href", ""),
                    "snippet": r.get("body", ""),  # DuckDuckGo Search returns 'body' instead of 'snippet'
                })
    except Exception as e:
        logging.exception("DuckDuckGo search failed: %s", e)
    return results

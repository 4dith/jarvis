# search.py
from ddgs import DDGS
import logging
from config import NUM_SEARCH_RESULTS

def ddg_search(query, top_k=NUM_SEARCH_RESULTS):
    results = []
    try:
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=top_k):
                results.append({
                    "title": r.get("title", ""),
                    "link": r.get("href", ""),
                    "snippet": r.get("body", "")
                })
    except Exception as e:
        logging.error(f"DDG search failed: {e}")

    if not results:
        logging.warning(f"No results found for: {query}")
    return results

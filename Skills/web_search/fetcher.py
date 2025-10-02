import requests
from bs4 import BeautifulSoup # type: ignore
import logging
from newspaper import Article # type: ignore

def fetch_page_text(url, timeout=15):
    """Return the main text extracted from the URL (best effort)."""
    try:
        headers = {"User-Agent": "Mozilla/5.0 (compatible; JARVIS/1.0)"}
        r = requests.get(url, headers=headers, timeout=timeout)
        r.raise_for_status()
        html = r.text
    except Exception as e:
        logging.exception("Failed to fetch %s: %s", url, e)
        return ""

    # Try newspaper3k if available for cleaner extraction
    try:
        a = Article(url)
        a.download(input_html=html)
        a.parse()
        text = a.text
        if text and len(text) > 50:
            return text
    except Exception:
        pass

    # Fallback: basic soup extraction
    soup = BeautifulSoup(html, "html.parser")
    # Remove scripts/styles
    for s in soup(["script", "style", "header", "footer", "nav", "aside"]):
        s.decompose()
    # Get paragraphs
    paragraphs = [p.get_text(separator=" ", strip=True) for p in soup.find_all("p")]
    text = "\n\n".join([p for p in paragraphs if len(p) > 40])
    return text
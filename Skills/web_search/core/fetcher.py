# fetcher.py
import requests, logging, time
from bs4 import BeautifulSoup
from newspaper import Article
from functools import lru_cache
from config import MAX_PAGES

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

@lru_cache(maxsize=128)
def fetch_page_text(url, timeout=15):
    """Fetch and clean webpage text with retries and caching."""
    headers = {"User-Agent": "Mozilla/5.0 (compatible; JARVIS/1.0)"}

    for attempt in range(3):
        try:
            r = requests.get(url, headers=headers, timeout=timeout)
            r.raise_for_status()
            html = r.text
            break
        except Exception as e:
            logging.warning(f"[Retry {attempt+1}] Failed to fetch {url}: {e}")
            time.sleep(1)
    else:
        return ""

    # Try Newspaper extraction first
    try:
        a = Article(url)
        a.download(input_html=html)
        a.parse()
        if len(a.text) > 100:
            return a.text
    except Exception:
        pass

    # Fallback with BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")
    for s in soup(["script", "style", "header", "footer", "nav", "aside"]):
        s.decompose()
    paragraphs = [p.get_text(" ", strip=True) for p in soup.find_all("p")]
    text = "\n".join([p for p in paragraphs if len(p) > 50])
    return text[:5000]  # Limit long pages

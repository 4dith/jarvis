# summarize.py
from transformers import pipeline
from functools import lru_cache
from config import SUMMARIZER_MODEL

@lru_cache(maxsize=1)
def _get_summarizer():
    """Load summarization pipeline once."""
    return pipeline("summarization", model=SUMMARIZER_MODEL)

def chunk_text(text, max_chars=1000):
    """Split long text into chunks."""
    return [text[i:i+max_chars] for i in range(0, len(text), max_chars)]

def summarize(text):
    summarizer = _get_summarizer()
    chunks = chunk_text(text)
    summaries = []
    for chunk in chunks:
        out = summarizer(chunk, max_length=130, min_length=30, do_sample=False)
        summaries.append(out[0]["summary_text"])
    return " ".join(summaries)

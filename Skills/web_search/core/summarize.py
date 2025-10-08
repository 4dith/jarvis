# core/summarize.py
import logging
from transformers import pipeline, AutoTokenizer
from functools import lru_cache
from config import SUMMARIZER_MODEL

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# ---------------------------------------------------
# ⚡ OPTIMIZATIONS APPLIED
# 1. Lazy loading & caching summarizer and tokenizer
# 2. Token-based chunking (not naive character split)
# 3. Dynamic summarization length (based on chunk size)
# 4. Batched inference → faster GPU/CPU utilization
# 5. Fallback to short snippet if summarization fails
# 6. Mixed precision (fp16) if GPU available
# ---------------------------------------------------

@lru_cache(maxsize=1)
def _load_summarizer():
    """Load summarization pipeline and tokenizer once."""
    logging.info(f"Loading summarizer model: {SUMMARIZER_MODEL}")
    summarizer = pipeline(
        "summarization",
        model=SUMMARIZER_MODEL,
        device_map="auto",
        torch_dtype="auto",  # Uses fp16 on GPU automatically
    )
    tokenizer = AutoTokenizer.from_pretrained(SUMMARIZER_MODEL)
    return summarizer, tokenizer


def _chunk_text(text, tokenizer, max_tokens=800):
    """Split text into token-based chunks for better accuracy."""
    tokens = tokenizer.encode(text)
    chunks = []
    for i in range(0, len(tokens), max_tokens):
        sub_tokens = tokens[i:i + max_tokens]
        chunk = tokenizer.decode(sub_tokens, skip_special_tokens=True)
        chunks.append(chunk)
    return chunks


def summarize(text, min_ratio=0.1, max_ratio=0.3):
    """
    Summarizes long text efficiently.
    - Uses dynamic chunking
    - Merges short outputs
    """
    summarizer, tokenizer = _load_summarizer()

    # Handle edge case
    if not text or len(text.strip()) < 60:
        return text.strip()

    chunks = _chunk_text(text, tokenizer)
    summaries = []

    try:
        # Batch process for speed
        results = summarizer(
            chunks,
            min_length=max(30, int(len(chunks[0].split()) * min_ratio)),
            max_length=max(80, int(len(chunks[0].split()) * max_ratio)),
            do_sample=False,
            truncation=True,
            batch_size=4,
        )
        summaries = [r["summary_text"].strip() for r in results]
    except Exception as e:
        logging.warning(f"Summarization failed: {e}")
        return text[:400] + "..."  # fallback snippet

    summary_text = " ".join(summaries)
    return summary_text.strip()

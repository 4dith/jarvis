import logging
from transformers import pipeline, AutoTokenizer
from functools import lru_cache
from config import SUMMARIZER_MODEL, MAX_SUMMARY_TOKENS

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# ---------------------------------------------------
# ⚡ OPTIMIZATIONS:
# 1. Lazy loading & caching of summarizer
# 2. Handles single combined text for concise summary
# 3. Truncates input text if too long for efficiency
# 4. Fallback to short snippet if summarization fails
# ---------------------------------------------------

@lru_cache(maxsize=1)
def _load_summarizer():
    """Load summarization pipeline once."""
    logging.info(f"Loading summarizer model: {SUMMARIZER_MODEL}")
    summarizer = pipeline(
        "summarization",
        model=SUMMARIZER_MODEL,
        device_map="auto",
        torch_dtype="auto",  # uses fp16 on GPU if available
    )
    tokenizer = AutoTokenizer.from_pretrained(SUMMARIZER_MODEL)
    return summarizer, tokenizer


def summarize(text, max_input_chars=3000, max_summary_tokens=MAX_SUMMARY_TOKENS):
    """
    Summarizes long text efficiently into a concise output.
    Args:
        text (str): Combined text from multiple sources
        max_input_chars (int): Truncate input to avoid very long texts
        max_summary_tokens (int): Maximum tokens for final summary
    Returns:
        str: Concise summary
    """
    summarizer, tokenizer = _load_summarizer()

    if not text or len(text.strip()) < 60:
        return text.strip()

    # Truncate text to avoid model overload
    text = text[:max_input_chars]

    try:
        summary = summarizer(
            text,
            max_length=max_summary_tokens,
            min_length=30,
            do_sample=False,
            truncation=True
        )[0]["summary_text"].strip()
    except Exception as e:
        logging.warning(f"Summarization failed: {e}")
        # fallback: first 300 chars
        return text[:300].rsplit('.', 1)[0] + "..."

    return summary

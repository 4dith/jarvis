import os
from typing import List
from transformers import pipeline

# Helper to chunk long text
def chunk_text(text, max_chars=800):
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + max_chars, len(text))
        chunk = text[start:end]
        chunks.append(chunk)
        start = end
    return chunks

# Hugging Face Summarizer
def summarize_with_hf(text, model_name="facebook/bart-large-cnn", max_length=120, min_length=30):
    summarizer = pipeline("summarization", model=model_name)
    chunks = chunk_text(text, max_chars=800)
    summaries = []
    for c in chunks:
        out = summarizer(c, max_length=max_length, min_length=min_length, do_sample=False)
        summaries.append(out[0]["summary_text"])
    return " ".join(summaries)

def summarize(text):
    return summarize_with_hf(text)
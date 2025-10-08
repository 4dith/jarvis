# config.py
# Central configuration for JARVIS

# Summarization model
SUMMARIZER_MODEL = "sshleifer/distilbart-cnn-12-6"

# SentenceTransformer model for reranking
RERANK_MODEL = "all-MiniLM-L6-v2"

# Number of search results to fetch
NUM_SEARCH_RESULTS = 6

# Maximum pages to fetch for summarization
MAX_PAGES = 3

# Maximum characters per summary
MAX_CHARS = 350

# Max workers for concurrent page fetching
MAX_WORKERS = 4

# Logging level
LOG_LEVEL = "INFO"

# JARVIS Web Search & Summarization

This project is a **JARVIS AI feature** that allows users to ask questions via **text or voice**, performs **web search**, summarizes the answers in a **ChatGPT-style format**, and provides the **source links**. Optional **voice output** can also read the summarized answer aloud.  

It is built entirely using **open-source tools** and **free technologies**, suitable for quick prototyping.

---

## 🚀 Features

- **Text or Voice Input**: Ask queries via text or record your voice.
- **Fast Web Search**: Fetches top relevant results from the web.
- **Summarization**: Generates concise answers using Hugging Face Transformers.
- **Source Links**: Shows the original URLs for transparency.
- **Voice Output (Optional)**: Reads the summarized answer aloud.
- **Open-Source & Free**: No paid APIs required.

---

## 🛠 Tech Stack

- **Python 3.10+**
- **Web Search**: `googlesearch-python` + `requests` + `BeautifulSoup`
- **Summarization**: Hugging Face Transformers (`facebook/bart-large-cnn`)
- **Voice Input**: OpenAI Whisper (`small` model)
- **Voice Output**: pyttsx3 (offline TTS)
- **GUI (Optional)**: Streamlit

---

## 📦 Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/jarvis-web-search.git
cd jarvis-web-search
pip install -r requirements.txt
```

2. requirements.txt
```
transformers
torch
requests
beautifulsoup4
googlesearch-python
pyttsx3
openai-whisper
streamlit  # optional
```


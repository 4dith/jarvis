# app.py
from flask import Flask, render_template, request
from core.handler import handler
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

app = Flask(__name__) 

@app.route("/", methods=["GET", "POST"])
def index():
    query = ""
    answer = ""
    sources = []

    if request.method == "POST":
        query = request.form.get("query", "").strip()
        if query:
            logging.info(f"User query: {query}")
            try:
                result = handler(query)
                answer = result.get("answer", "")
                sources = result.get("sources", [])
            except Exception as e:
                logging.exception("Error processing query")
                answer = "⚠️ Sorry, an error occurred while processing your query."
                sources = []

    return render_template(
        "index.html",
        answer=answer,
        sources=sources,
        query=query
    )

if __name__ == "__main__":
    # Run on all interfaces for easier local network testing
    app.run(host="0.0.0.0", port=8000, debug=True)

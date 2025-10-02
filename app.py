from flask import Flask, render_template, request
from Skills.web_search.handler import handler
import logging

app = Flask(__name__)

# Suppress verbose logs
logging.getLogger().setLevel(logging.CRITICAL)

@app.route("/", methods=["GET", "POST"])
def index():
    query = ""
    answer = ""
    sources = []
    meta = {}

    if request.method == "POST":
        query = request.form.get("query", "").strip()
        if query:
            try:
                result = handler(query)
                answer = result.get("answer", "No answer found.")
                sources = result.get("sources", [])
                meta = result.get("meta", {})
            except Exception as e:
                answer = f"An error occurred: {str(e)}"
                sources = []
    
    return render_template(
        "result.html", 
        query=query, 
        answer=answer, 
        sources=sources,
        meta=meta
    )

if __name__ == "__main__":
    app.run(debug=True)

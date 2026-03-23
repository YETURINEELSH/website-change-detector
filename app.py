from flask import Flask, request, jsonify, render_template
import requests
import difflib
import os
import json
from datetime import datetime
from bs4 import BeautifulSoup

app = Flask(__name__)

DATA_FILE = "data.json"

# ---------------------------
# Utility Functions
# ---------------------------

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

# Clean HTML
def extract_text(html):
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    text = soup.get_text(separator=" ")
    return " ".join(text.split())

# Fetch content
def fetch_content(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers, timeout=10)
    return extract_text(response.text)

# AI-like summary
def summarize_changes(diff):
    added = sum(1 for d in diff if d.startswith("+"))
    removed = sum(1 for d in diff if d.startswith("-"))

    if added == 0 and removed == 0:
        return "No significant content changes detected."

    if added > 20 or removed > 20:
        return "Major update detected: significant content added or removed."

    return "Minor update: small text changes detected."

# ---------------------------
# Routes
# ---------------------------

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/add", methods=["POST"])
def add_url():
    url = request.json.get("url")
    data = load_data()

    content = fetch_content(url)

    if url not in data:
        data[url] = []

    data[url].append({
        "timestamp": str(datetime.now()),
        "content": content
    })

    save_data(data)
    return jsonify({"message": "URL added successfully"})

@app.route("/check", methods=["POST"])
def check_changes():
    url = request.json.get("url")
    data = load_data()

    if url not in data or len(data[url]) == 0:
        return jsonify({"error": "URL not found"}), 404

    old_content = data[url][-1]["content"]
    new_content = fetch_content(url)

    diff = list(difflib.ndiff(old_content.split(), new_content.split()))
    changes = [d for d in diff if d.startswith("+ ") or d.startswith("- ")]

    change_type = "minor"
    if len(changes) > 50:
        change_type = "major"

    summary = summarize_changes(changes)

    data[url].append({
        "timestamp": str(datetime.now()),
        "content": new_content
    })

    save_data(data)

    return jsonify({
        "summary": summary,
        "type": change_type,
        "changes": changes[:50]
    })

# ---------------------------
# ✅ CORRECT PLACE FOR RUN
# ---------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
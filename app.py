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

# ✅ Clean HTML (IMPORTANT FIX)
def extract_text(html):
    soup = BeautifulSoup(html, "html.parser")

    # Remove scripts and styles
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    text = soup.get_text(separator=" ")
    return " ".join(text.split())  # remove extra spaces

# ✅ Fetch with headers (avoid bot detection)
def fetch_content(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    response = requests.get(url, headers=headers, timeout=10)
    return extract_text(response.text)

# ---------------------------
# AI-like Summary (Rule-based)
# ---------------------------

def summarize_changes(diff):
    added = sum(1 for d in diff if d.startswith("+"))
    removed = sum(1 for d in diff if d.startswith("-"))

    if added == 0 and removed == 0:
        return "No significant content changes detected."

    if added > 20 or removed > 20:
        return "Major update detected: significant content added or removed."

    if added > 0 or removed > 0:
        return "Minor update: small text changes detected."

    return "Changes detected."

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
    timestamp = str(datetime.now())

    if url not in data:
        data[url] = []

    data[url].append({
        "timestamp": timestamp,
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

    # Keep only meaningful changes
    changes = [d for d in diff if d.startswith("+ ") or d.startswith("- ")]

    # Classification
    change_type = "minor"
    if len(changes) > 50:
        change_type = "major"

    # AI-like summary
    summary = summarize_changes(changes)

    # Save new version
    data[url].append({
        "timestamp": str(datetime.now()),
        "content": new_content
    })

    save_data(data)

    return jsonify({
        "summary": summary,
        "type": change_type,
        "changes": changes[:50]  # limit output
    })

# ---------------------------

if __name__ == "__main__":
    app.run(debug=True)
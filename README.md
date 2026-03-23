# 🌐 Intelligent Website Change Detection System

## 🚀 Overview

The **Intelligent Website Change Detection System** is a web-based application that monitors websites for content updates, detects differences between versions, and provides intelligent summaries of changes.

This system helps businesses track competitor websites, news updates, and important content changes automatically without manual effort.

---

## 🎯 Features

* 🔗 Add and monitor any website URL
* ⏱ Periodically fetch website content
* 🔍 Detect changes between versions
* 🧠 AI-like summary of changes
* 🟡 Classify changes as **Minor** or **Major**
* 📜 Maintain version history
* ⚡ Fast and lightweight system

---

## 🧠 How It Works

1. User adds a website URL
2. System fetches and stores website content
3. On each check:

   * New content is fetched
   * Compared with previous version
   * Differences are detected
4. Changes are:

   * Filtered (removes scripts/styles)
   * Classified (minor/major)
   * Summarized intelligently

---

## 🛠 Tech Stack

* **Frontend:** HTML, CSS, JavaScript
* **Backend:** Python (Flask)
* **Libraries:**

  * requests
  * BeautifulSoup
  * difflib

---

## 📂 Project Structure

```
website-change-detector/
│
├── app.py
├── requirements.txt
├── data.json
├── templates/
│   └── index.html
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository

```
git clone https://github.com/YOUR_USERNAME/website-change-detector.git
cd website-change-detector
```

### 2️⃣ Install dependencies

```
pip install -r requirements.txt
```

### 3️⃣ Run the application

```
python app.py
```

### 4️⃣ Open in browser

```
http://127.0.0.1:5000
```

---

## 🧪 Usage

1. Enter a website URL
2. Click **Add URL**
3. Wait a few minutes
4. Click **Check Changes**
5. View:

   * Change summary
   * Type (Minor/Major)
   * Detected differences

---

## 🌍 Demo Websites

For testing, use:

* https://news.ycombinator.com
* https://example.com
* https://wikipedia.org

---

## ⚠️ Limitations

* Some websites block scraping (Cloudflare, CAPTCHA)
* Dynamic content may vary slightly between requests
* Currently uses rule-based summarization (can be upgraded with AI APIs)

---

## 🔮 Future Enhancements

* 🤖 Real AI integration (OpenAI)
* 📊 Visual dashboard with graphs
* 🔔 Email/notification alerts
* 🕒 Automatic scheduled monitoring
* 🌐 Chrome extension

---

## 🏆 Hackathon Value

This project demonstrates:

* Real-world problem solving
* Web scraping & data processing
* Change detection algorithms
* Intelligent summarization

---

## 👨‍💻 Author

**Your Name**
GitHub: https://github.com/YETURINEELESH

---

## ⭐ If you like this project

Give it a ⭐ on GitHub!

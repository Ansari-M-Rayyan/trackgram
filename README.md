# TrackGram 🔎
### Tactical OSINT Intelligence & Behavioral Profiling Dashboard

**TrackGram** is a sophisticated Open Source Intelligence (OSINT) platform designed for deep-dive analysis of Instagram profiles. By utilizing a "Bring Your Own Data" (BYOD) architecture, TrackGram bypasses traditional scraping limitations. It transforms raw metadata into actionable intelligence using Natural Language Processing (NLP), Computer Vision, and Behavioral Heuristics.

---

## 🚀 Key Features

### 📡 Tactical Data Extraction
* **Ghost Extractor (Bookmarklet):** A stealthy, client-side extraction tool that leverages the user's active browser session to bypass Instagram's firewall and export profile data as a JSON payload.
* **Air-Gapped Analysis:** No direct connection between the server and Instagram, ensuring your IP address remains clean and untraceable.

### 🧠 AI-Driven Synthesis
* **Bot Scorer (Random Forest):** Uses machine learning to evaluate followers, following ratios, and posting volume to assign a "Bot Probability" score.
* **NLP Intent Modeling (RoBERTa):** Zero-shot classification of captions to detect themes like financial scams, political influence, or promotional spam.
* **Linguistic Sentiment Analysis:** Maps the emotional tone and "vibe" of the target's communication over time.

### 📊 Intelligence Sections
* **A. Account Metadata:** Core identifiers including Internal Numeric IDs and bio-link tracking.
* **B. Content Analysis:** Classification of media types (Reels vs. Images) and timeline continuity heuristics (detecting deleted content).
* **C. Behavioral Profiling:** "Pattern of Life" mapping, detecting peak activity hours and automation spikes.
* **D. Network Mapping:** Visualization of most-frequently tagged accounts and hashtags to identify the target's primary circle of influence.

---

## 🛠️ Tech Stack

**Frontend:**
* React.js (Vite)
* Tailwind CSS (Dashboard Styling)
* Lucide React (Icons)

**Backend:**
* FastAPI (Python)
* Uvicorn (Server)
* Scikit-Learn (ML Classification)
* HuggingFace Transformers (NLP Zero-Shot)
* TextBlob (Sentiment Analysis)

---

## 📦 Installation & Setup

### 1. Prerequisites
* **Node.js:** v20+ recommended.
* **Python:** 3.9+ recommended.

### 2. The Ghost Extractor (Bookmarklet Setup)
To acquire data, you must create a browser bookmarklet. This allows you to extract data while logged into your own account, bypassing bot detection.

1. Create a new bookmark in your browser.
2. Name it `TrackGram Extractor`.
3. Paste the following into the **URL** field:

```javascript
javascript:(function(){
    let username = window.location.pathname.replace(/\//g, '');
    if(!username) { alert('Go to an Instagram profile first!'); return; }
    fetch('https://i.instagram.com/api/v1/users/web_profile_info/?username=' + username, {
        headers: { 'x-ig-app-id': '936619743392459' }
    })
    .then(res => res.json())
    .then(data => {
        let payload = {
            extracted_at: new Date().toISOString(),
            data: data.data
        };
        let blob = new Blob([JSON.stringify(payload, null, 2)], {type: 'application/json'});
        let a = document.createElement('a');
        a.href = URL.createObjectURL(blob);
        a.download = username + '_osint_payload.json';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
    })
    .catch(err => alert('Extraction blocked. Refresh the page and try again.'));
})();
```

### 3. Backend Setup
```bash
cd backend
# Create a requirements.txt with the dependencies listed below
pip install -r requirements.txt
python main.py
```
*The server will boot on `http://localhost:8000`. AI models will download on the first run.*

### 4. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
*The dashboard will boot on `http://localhost:5173`.*

---

## 📖 Usage Guide

1. **Extract:** Visit a public Instagram profile and click your `TrackGram Extractor` bookmark.
2. **Inject:** Drag the resulting `.json` file into the TrackGram dashboard.
3. **Analyze:** Review the tactical analysis synthesized by the AI models.
4. **Report:** Click **"Download PDF Report"** to export a formatted intelligence dossier.

---

## 📄 Backend Requirements (`requirements.txt`)
Paste the following into your `backend/requirements.txt` file:
```text
fastapi
uvicorn
python-multipart
textblob
transformers
scikit-learn
torch
torchvision
pillow
requests
pydantic
```

---

## ⚖️ Disclaimer
This tool is intended for **educational and research purposes only**. Users are responsible for adhering to the Terms of Service of the platforms they analyze and local laws regarding data privacy.

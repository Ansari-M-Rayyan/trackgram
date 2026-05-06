# TrackGram 🔎

## Advanced OSINT Forensic Profiling & Neural Intelligence Dashboard
#### TrackGram is a next-generation Digital Forensic and Open Source Intelligence (OSINT) suite. By combining a Bring Your Own Data (BYOD) architecture with local Large Language Models (LLMs), TrackGram generates comprehensive behavioral and environmental dossiers without ever exposing your network identity to the target platform.
---

## 🚀 Key Features

### 📡 Deep-Stream Interceptor (Ghost Extractor v2)
#### High-Fidelity Interception: A specialized client-side tool that captures rich API metadata, including hidden Felix Video Timelines and deep link arrays often missed by standard scrapers.

#### Privacy-First Extraction: Leverages active browser sessions to acquire data securely, bypassing advanced bot detection and TLS fingerprinting.

### 🧠 Local Neural Engine (Llama 3.2)
#### Zero-Hallucination Intelligence: Powered by locally hosted LLMs via Ollama. It performs cold, clinical reasoning on target data with optimized parameters for maximum factual reliability.

#### Forensic Reporting: Automatically synthesizes data into structured briefing documents: Identity & Environment, Network Coherence, and Forensic Verdicts.

### 👁️ Digital Environment Recon (Vision AI)
#### Scene Classification: Uses Vision Transformers (ViT) to analyze profile imagery, identifying professional environments such as PODIUMS, AUDITORIUMS, or PRESS CONFERENCES.

#### Contextual Validation: Cross-references visual environmental tags against claimed professional identity to detect anomalies or deep-cover inconsistencies.

### 📊 Intelligence Modules
#### Network Associates Mapping: Deep extraction of @mentions across all media types (Posts, Reels, IGTV) to map high-value connections and institutional affiliations.

#### Thematic Topic Clustering: Analyzes hashtag frequency and caption semantics to identify the target's primary narrative and circle of influence.

#### Legitimacy Heuristics: A multi-factor scoring system evaluating verified status, follower-to-following ratios, and engagement continuity.

---

## 🛠️ Tech Stack

**Frontend:**
* React.js (Vite)
* Tailwind CSS (Dashboard Styling)
* Lucide React

**Backend:**
* FastAPI (Python)
* Ollama (Llama 3.2)
* HuggingFace Transformers (ViT)
* NVIDIA CUDA
* Pillow & Requests

---

## 📦 Installation & Setup

### 1. Prerequisites
* **Node.js:** v20+ recommended.
* **Python:** 3.9+ recommended.
* **Ollama:** Required for local LLM inference (Llama 3.2)

### 2. The Ghost Extractor (Bookmarklet Setup)
To acquire data, you must create a browser bookmarklet. This allows you to extract data while logged into your own account, bypassing bot detection.

1. Create a new bookmark in your browser.
2. Name it `TrackGram Extractor`.
3. Paste the following into the **URL** field:

```javascript
javascript:(function(){     let username = window.location.pathname.replace(/\//g, '');     if(!username || username === 'reels' || username === 'explore') {          alert('Navigate to a specific Profile first!'); return;      }          console.log('%F0%9F%93%A1 TrackGram: Initiating Forensic Extraction for @' + username);      fetch(`https://i.instagram.com/api/v1/users/web_profile_info/?username=${username}`,%20{%20%20%20%20%20%20%20%20%20headers:%20{%20%20%20%20%20%20%20%20%20%20%20%20%20%27x-ig-app-id%27:%20%27936619743392459%27,%20%20%20%20%20%20%20%20%20%20%20%20%20%27sec-ch-ua-platform%27:%20%27%22Windows%22%27,%20%20%20%20%20%20%20%20%20%20%20%20%20%27User-Agent%27:%20navigator.userAgent%20%20%20%20%20%20%20%20%20}%20%20%20%20%20})%20%20%20%20%20.then(res%20=%3E%20{%20%20%20%20%20%20%20%20%20if(res.status%20===%20429)%20throw%20new%20Error(%27Rate%20limited.%20Wait%205%20mins.%27);%20%20%20%20%20%20%20%20%20if(!res.ok)%20throw%20new%20Error(%27Access%20Denied/Private%20Profile.%27);%20%20%20%20%20%20%20%20%20return%20res.json();%20%20%20%20%20})%20%20%20%20%20.then(json%20=%3E%20{%20%20%20%20%20%20%20%20%20let%20payload%20=%20{%20%20%20%20%20%20%20%20%20%20%20%20%20metadata:%20{%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20target:%20username,%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20extracted_at:%20new%20Date().toISOString(),%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20tool:%20%22TrackGram%20v2%20(RTX-Llama)%22%20%20%20%20%20%20%20%20%20%20%20%20%20},%20%20%20%20%20%20%20%20%20%20%20%20%20data:%20json.data%20%20%20%20%20%20%20%20%20};%20%20%20%20%20%20%20%20%20%20let%20blob%20=%20new%20Blob([JSON.stringify(payload,%20null,%202)],%20{type:%20%27application/json%27});%20%20%20%20%20%20%20%20%20let%20a%20=%20document.createElement(%27a%27);%20%20%20%20%20%20%20%20%20a.href%20=%20URL.createObjectURL(blob);%20%20%20%20%20%20%20%20%20a.download%20=%20`TG_Dossier_${username}_${Date.now()}.json`;%20%20%20%20%20%20%20%20%20document.body.appendChild(a);%20%20%20%20%20%20%20%20%20a.click();%20%20%20%20%20%20%20%20%20document.body.removeChild(a);%20%20%20%20%20%20%20%20%20console.log(%27%E2%9C%85%20Extraction%20Complete.%20File%20ready%20for%20Llama%20analysis.%27);%20%20%20%20%20})%20%20%20%20%20.catch(err%20=%3E%20alert(%27%E2%9D%8C%20TrackGram%20Error:%20%27%20+%20err.message));%20})();
```

### 3. Backend Setup
```bash
# Ensure Ollama is running Llama 3.2
ollama run llama3.2

cd backend
# Install Python dependencies
pip install -r requirements.txt
# Launch the inference engine
python main.py
```
*The server will boot on http://localhost:8000. Neural weights and Vision Transformers will initialize on the first run.*

### 4. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
*The dashboard will boot.*

---

## 📖 Usage Guide

1. **Extract:** Visit a public Instagram profile and click your `TrackGram Extractor` bookmark.
2. **Inject:** Drag the resulting `.json` file into the TrackGram dashboard.
3. **Analyze:** Review the tactical analysis synthesized by the AI models (Llama 3.2 & ViT).
4. **Report:** Click **"Download PDF Report"** to export a formatted intelligence dossier.

---

## 📄 Backend Requirements (`requirements.txt`)
Paste the following into your `backend/requirements.txt` file:
```text
fastapi
uvicorn
python-multipart
requests
torch
torchvision
transformers
huggingface_hub
scikit-learn
numpy
pillow
```

---

## ⚖️ Disclaimer
This tool is intended for **educational and research purposes only**. Users are responsible for adhering to the Terms of Service of the platforms they analyze and local laws regarding data privacy.

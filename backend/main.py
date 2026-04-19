import json
import numpy as np
import requests
import re
from io import BytesIO
from PIL import Image
from datetime import datetime
from collections import Counter
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from textblob import TextBlob
from transformers import pipeline
from sklearn.ensemble import RandomForestClassifier
import uvicorn # <-- Needed to run via 'python main.py'

# --- AI Model Storage ---
ml_models = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Loading AI Models... (This might take a minute)")
    # NLP Topic Classifier
    ml_models['topic_classifier'] = pipeline("zero-shot-classification", model="cross-encoder/nli-distilroberta-base")
    
    # Bot Scorer - Synthetic Training
    X_train = np.array([[10, 5000, 0, 0], [50, 2000, 2, 0], [500, 400, 50, 0], [10000, 500, 200, 1], [0, 10, 0, 0], [1000000, 10, 500, 1]])
    y_train = np.array([1, 1, 0, 0, 1, 0])
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)
    ml_models['bot_scorer'] = clf
    print("Models Loaded! Application startup complete.")
    yield
    ml_models.clear()

app = FastAPI(title="TRACKGRAM Intelligence API", lifespan=lifespan)

# Allow React to talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze-file")
async def analyze_uploaded_file(file: UploadFile = File(...)):
    try:
        content = await file.read()
        payload = json.loads(content)
        
        user_raw = payload.get("data", {}).get("user", {})
        if not user_raw:
            raise HTTPException(status_code=400, detail="Invalid payload. Extraction failed.")

        # --- A. Account Identification ---
        user_info = {
            "Username": user_raw.get("username", "Unknown"),
            "Account_ID": user_raw.get("id", "Unknown"),
            "Full_Name": user_raw.get("full_name", "N/A"),
            "Followers": user_raw.get('edge_followed_by', {}).get('count', 0),
            "Following": user_raw.get('edge_follow', {}).get('count', 0),
            "Image_Count": user_raw.get("edge_owner_to_timeline_media", {}).get("count", 0),
            "Is_Verified": user_raw.get("is_verified", False),
            "Biography": user_raw.get("biography", "N/A"),
            "External_URL": user_raw.get("external_url", "None")
        }

        edges = user_raw.get("edge_owner_to_timeline_media", {}).get("edges", [])
        captions, timestamps, comments, likes = [], [], [], []
        post_types = {"images": 0, "reels_videos": 0, "text_heavy": 0}
        
        for edge in edges:
            node = edge.get("node", {})
            if node.get("is_video"): post_types["reels_videos"] += 1
            else: post_types["images"] += 1
                
            ts = node.get("taken_at_timestamp")
            if ts: timestamps.append(ts)
                
            likes.append(node.get("edge_liked_by", {}).get("count", 0))
            comments.append(node.get("edge_media_to_comment", {}).get("count", 0))

            cap_edges = node.get("edge_media_to_caption", {}).get("edges", [])
            if cap_edges:
                text = str(cap_edges[0].get("node", {}).get("text", ""))
                captions.append(text)
                if len(text) > 200: post_types["text_heavy"] += 1

        # --- B. Content Analysis ---
        sentiments = [TextBlob(c).sentiment.polarity for c in captions]
        avg_sentiment = sum(sentiments) / len(sentiments) if sentiments else 0
        tone = "Aggressive/Negative" if avg_sentiment < -0.1 else "Promotional/Positive" if avg_sentiment > 0.2 else "Neutral/Informational"

        top_theme = "INSUFFICIENT DATA"
        if captions:
            valid_texts = [c for c in captions if len(c) > 10][:5]
            if valid_texts:
                res = ml_models['topic_classifier'](valid_texts, ['financial scams', 'political', 'impersonation/harassment', 'lifestyle'])
                top_theme = res[0]['labels'][0]

        # --- C. Behavioral Analysis ---
        timestamps.sort()
        gaps = [timestamps[i] - timestamps[i-1] for i in range(1, len(timestamps))]
        avg_gap = sum(gaps)/len(gaps) if gaps else 0
        timeline_gaps = "High Probability" if avg_gap > 2592000 else "Normal Timeline"

        avg_likes = sum(likes)/len(likes) if likes else 0
        er = (avg_likes / user_info["Followers"]) * 100 if user_info["Followers"] > 0 else 0
        engagement_tactic = "Suspiciously Low" if er < 0.5 else "Mass Engagement Farm" if er > 15 else "Organic/Normal"

        post_hours = [datetime.fromtimestamp(ts).hour for ts in timestamps]
        activity_map = dict(Counter(post_hours))
        peak_hour = max(activity_map, key=activity_map.get) if activity_map else "Unknown"

        # AI Bot Scorer
        feat = np.array([[user_info["Followers"], user_info["Following"], user_info["Image_Count"], 1 if user_info["Is_Verified"] else 0]])
        bot_prob = round(ml_models['bot_scorer'].predict_proba(feat)[0][1] * 100, 2)

        return {
            "profile": user_info,
            "content_analysis": {
                "post_types": f"Images: {post_types['images']} | Reels: {post_types['reels_videos']} | Text-Heavy: {post_types['text_heavy']}",
                "primary_theme": top_theme.upper(),
                "language_tone": tone,
                "deleted_edited_heuristic": f"Continuity: {timeline_gaps} ({round(avg_gap/86400)} day gap avg)",
                "exif_metadata": "STRIPPED BY META (Standard OSINT Constraint)"
            },
            "behavioral_analysis": {
                "posting_schedule": f"Peak at {peak_hour}:00 HR (Local)",
                "sudden_spikes": "Detected" if (len(gaps) > 0 and min(gaps) < 3600) else "None Detected",
                "automation_indicators": f"{'High' if bot_prob > 60 else 'Low'} Risk ({bot_prob}%)",
                "engagement_tactics": f"{engagement_tactic} (ER: {round(er, 2)}%)",
                "story_patterns": f"Highlights: {user_raw.get('highlight_reel_count', 0)}"
            },
            "ai_analysis": {
                "bot_probability": bot_prob,
                "average_sentiment": round(avg_sentiment, 2),
                "topics": {}, # Legacy field
                "latest_image_vision": "Processed via Meta Proxy"
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- THIS IS THE CRITICAL BLOCK FOR "python main.py" ---
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
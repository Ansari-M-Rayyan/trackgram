import json
import requests
import re
import torch
import uvicorn
from io import BytesIO
from PIL import Image
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from transformers import pipeline
from huggingface_hub import login

# --- SYSTEM CONFIGURATION ---
HF_TOKEN = "Enter your Hugging Face API Token here" 
login(token=HF_TOKEN)

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
ml_models = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    device = 0 if torch.cuda.is_available() else -1
    gpu_status = torch.cuda.get_device_name(0) if device == 0 else "System CPU"
    try:
        check = requests.get("http://127.0.0.1:11434/api/tags", timeout=5)
        available = [m['name'] for m in check.json().get('models', [])]
        ml_models['llama_name'] = next((x for x in available if "llama3.2" in x), "llama3.2:latest")
    except:
        ml_models['llama_name'] = "llama3.2:latest"
        
    print(f"🚀 TrackGram Engine: {gpu_status} | Target LLM: {ml_models['llama_name']}")
    ml_models['vision'] = pipeline("image-classification", model="google/vit-base-patch16-224", device=device)
    yield
    ml_models.clear()

app = FastAPI(title="TrackGram Intelligence Core", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

def get_deep_data(user_obj):
    """
    Forensically crawls the entire JSON object to find every caption, mention, and hashtag
    even if they are hidden in Video, Reels, or Sidecar arrays.
    """
    all_captions = []
    
    # 1. Standard Posts
    timeline = user_obj.get("edge_owner_to_timeline_media", {}).get("edges", [])
    # 2. Video/Reels 
    videos = user_obj.get("edge_felix_video_timeline", {}).get("edges", [])
    
    combined_nodes = timeline + videos
    
    for edge in combined_nodes:
        node = edge.get("node", {})
        # Capture captions from standard and nested structures
        caps = node.get("edge_media_to_caption", {}).get("edges", [])
        if caps:
            all_captions.append(caps[0].get("node", {}).get("text", ""))

    full_text = " ".join(all_captions)
    
    # Deep Regex Extraction
    mentions = sorted(list(set(re.findall(r"@([\w\.]+)", full_text))))
    hashtags = sorted(list(set(re.findall(r"#([\w\.]+)", full_text))))
    
    return mentions, hashtags, combined_nodes

def query_llama_investigator(data_packet):
    prompt = f"""
SYSTEM: You are a Lead Digital Forensic Analyst. Analyze this target dossier:
{data_packet}

TASK: Generate a professional Forensic Report.
1. IDENTITY & ENVIRONMENT: Analyze bio and visual context. Explain if 'podium/stage' vision tags support their public office.
2. NETWORK COHERENCE: Analyze if mentioned associates (like PMOIndia or foreign ministers) confirm their professional status.
3. FORENSIC VERDICT: Final reliability statement.

FORMAT: Use ### headers. Be clinical and factual.
"""
    payload = {"model": ml_models.get("llama_name"), "prompt": prompt, "stream": False, "options": {"temperature": 0.0}}
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=180)
        return response.json().get("response", "AI failed to generate text.")
    except Exception as e: return f"Forensic Bridge Error: {str(e)}"

@app.post("/analyze-file")
async def analyze(file: UploadFile = File(...)):
    try:
        content = await file.read()
        raw_json = json.loads(content)
        user = raw_json.get("data", {}).get("user", {})
        
        if not user: raise HTTPException(status_code=400, detail="Invalid Target Payload")

        # --- DEEP EXTRACTION ---
        mentions, hashtags, nodes = get_deep_data(user)
        
        # --- VISION RECON (Multi-Image Context) ---
        vision_results = []
        headers = {"User-Agent": "Mozilla/5.0"}
        
        # Analyze up to the 3 most recent images for better environment context
        for i in range(min(3, len(nodes))):
            try:
                img_url = nodes[i]['node']['display_url']
                img_res = requests.get(img_url, headers=headers, timeout=5)
                if img_res.status_code == 200:
                    img = Image.open(BytesIO(img_res.content)).convert("RGB")
                    preds = ml_models['vision'](img, top_k=3)
                    vision_results.extend([p['label'].split(',')[0].upper() for p in preds])
            except: continue
        
        vision_tags = list(set(vision_results)) if vision_results else ["NO_VISUAL_DATA"]

        # --- LEGITIMACY CALCULATION ---
        followers = user.get('edge_followed_by', {}).get('count', 0)
        is_verified = user.get("is_verified", False)
        legitimacy = 100 if is_verified else (90 if followers > 10000 else 70)

        # --- GENERATE DOSSIER ---
        dossier_data = {
            "handle": user.get("username"),
            "bio": user.get("biography"),
            "followers": followers,
            "vision_context": vision_tags,
            "network_mentions": mentions[:15], # Show more to Llama
            "thematic_topics": hashtags[:15]
        }
        
        report = query_llama_investigator(json.dumps(dossier_data))

        return {
            "identity": {
                "handle": f"@{user.get('username')}",
                "name": user.get("full_name"),
                "status": "VERIFIED_ENTITY" if is_verified else "UNVERIFIED_ACCOUNT"
            },
            "forensics": {
                "legitimacy_score": legitimacy,
                "environment": vision_tags,
                "report": report,
                "hardware": torch.cuda.get_device_name(0) if torch.cuda.is_available() else "System CPU"
            },
            "network": {
                "mentions": mentions[:10], # Indepth list for Frontend
                "topics": hashtags[:10]   # Indepth list for Frontend
            }
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000)

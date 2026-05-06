import requests
import json
import time

def check_ollama_health():
    print("🔍 STEP 1: Checking if Ollama is running on port 11434...")
    try:
        # Check if the service is alive
        res = requests.get("http://127.0.0.1:11434/", timeout=5)
        print(f"✅ Ollama Service: {res.text}")
    except Exception as e:
        print(f"❌ Ollama is NOT running. Error: {e}")
        return

    print("\n🔍 STEP 2: Checking available models...")
    try:
        res = requests.get("http://127.0.0.1:11434/api/tags", timeout=5)
        models = [m['name'] for m in res.json().get('models', [])]
        print(f"📦 Installed Models: {models}")
        
        if not models:
            print("❌ No models found. Run 'ollama run llama3.2' first.")
            return
        
        # Select the first model that looks like Llama 3.2
        target_model = next((x for x in models if "llama3.2" in x), models[0])
        print(f"🎯 Target Model for test: {target_model}")
    except Exception as e:
        print(f"❌ Failed to list models: {e}")
        return

    print(f"\n🔍 STEP 3: Testing AI Reasoning (Llama 3.2)...")
    payload = {
        "model": target_model,
        "prompt": "Say 'Connection Successful' if you can read this.",
        "stream": False
    }
    
    start_time = time.time()
    try:
        # No timeout here to see how long your hardware actually takes
        response = requests.post("http://127.0.0.1:11434/api/generate", json=payload)
        
        if response.status_code == 200:
            ai_reply = response.json().get("response")
            duration = round(time.time() - start_time, 2)
            print(f"✅ AI REPLY: {ai_reply}")
            print(f"⏱️ INFERENCE TIME: {duration} seconds")
        else:
            print(f"❌ Ollama Error Code: {response.status_code}")
    except Exception as e:
        print(f"❌ Post request failed: {e}")

if __name__ == "__main__":
    check_ollama_health()
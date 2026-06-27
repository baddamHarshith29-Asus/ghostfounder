# ─────────────────────────────────────────────
# FEATURE 1: FOUNDER MEMORY (using Hindsight & Local fallback)
# Remembers every decision across sessions
# ─────────────────────────────────────────────
import json
import os
from datetime import datetime
from utils.helpers import get_env

# Attempt to import Hindsight client from Hindsight SDK (support both new & legacy SDK versions)
try:
    from hindsight_client import Hindsight
    HINDSIGHT_AVAILABLE = True
    HINDSIGHT_SDK_NEW = True
except ImportError:
    try:
        from hindsight import HindsightClient
        HINDSIGHT_AVAILABLE = True
        HINDSIGHT_SDK_NEW = False
    except ImportError:
        HINDSIGHT_AVAILABLE = False
        HINDSIGHT_SDK_NEW = False

MEMORY_FILE = "data/memory_store.json"

def _load_memory():
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def _save_memory(data):
    os.makedirs("data", exist_ok=True)
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=2)

def classify_category(content: str) -> str:
    """Classify the content into a startup category based on keywords"""
    text = content.lower()
    if any(w in text for w in ["price", "pricing", "discount", "cheaper", "undercut", "cost", "revenue", "charge"]):
        return "Pricing"
    if any(w in text for w in ["feature", "app", "build", "product", "ui", "code", "dev", "design", "launch"]):
        return "Product"
    if any(w in text for w in ["market", "marketing", "user", "customer", "ad", "ads", "acquisition", "sales"]):
        return "Marketing"
    if any(w in text for w in ["funding", "invest", "vc", "seed", "bootstrap", "runway", "burn", "budget", "money"]):
        return "Finance"
    if any(w in text for w in ["hire", "firing", "employee", "team", "cofounder", "co-founder", "salary"]):
        return "Team"
    return "General"

def save_decision(user_id: str, content: str, category: str = None, type_tag: str = "decision"):
    """Save a decision or conversation to memory"""
    if not category:
        category = classify_category(content)
        
    timestamp = datetime.now().isoformat()
    
    # Try Hindsight if configured
    hindsight_api_key = get_env("HINDSIGHT_API_KEY")
    hindsight_pipeline_id = get_env("HINDSIGHT_PIPELINE_ID")
    
    saved_to_hindsight = False
    if HINDSIGHT_AVAILABLE and hindsight_api_key and hindsight_pipeline_id:
        try:
            if HINDSIGHT_SDK_NEW:
                client = Hindsight(base_url="https://api.hindsight.vectorize.io", api_key=hindsight_api_key)
                client.retain(
                    bank_id=hindsight_pipeline_id,
                    content=f"[{category}][{type_tag}] {content}",
                    tags=[user_id]
                )
            else:
                client = HindsightClient(api_key=hindsight_api_key)
                client.retain(
                    pipeline_id=hindsight_pipeline_id,
                    user_id=user_id,
                    content=f"[{category}][{type_tag}] {content}"
                )
            saved_to_hindsight = True
        except Exception:
            pass  # Fall back to local storage if API call fails
            
    # Always save locally as a reliable source of structured logs for the UI
    memory = _load_memory()
    if user_id not in memory:
        memory[user_id] = []
    
    memory[user_id].append({
        "content": content,
        "category": category,
        "type": type_tag,
        "timestamp": timestamp,
        "hindsight_stored": saved_to_hindsight
    })
    _save_memory(memory)

def recall_decisions(user_id: str, query: str = "", category: str = None, top_k: int = 5):
    """Recall relevant past decisions"""
    # Try using Hindsight if configured
    hindsight_api_key = get_env("HINDSIGHT_API_KEY")
    hindsight_pipeline_id = get_env("HINDSIGHT_PIPELINE_ID")
    
    if HINDSIGHT_AVAILABLE and hindsight_api_key and hindsight_pipeline_id:
        try:
            if HINDSIGHT_SDK_NEW:
                client = Hindsight(base_url="https://api.hindsight.vectorize.io", api_key=hindsight_api_key)
                response = client.recall(
                    bank_id=hindsight_pipeline_id,
                    query=query,
                    tags=[user_id]
                )
                if response and response.results:
                    return [r.text.split("] ", 1)[-1] if "] " in r.text else r.text for r in response.results]
            else:
                client = HindsightClient(api_key=hindsight_api_key)
                results = client.recall(
                    pipeline_id=hindsight_pipeline_id,
                    user_id=user_id,
                    query=query,
                    top_k=top_k
                )
                if results:
                    # Clean prefix tags if any
                    return [r.split("] ", 1)[-1] if "] " in r else r for r in results]
        except Exception:
            pass


    # Local fallback search
    memory = _load_memory()
    entries = memory.get(user_id, [])
    if not entries:
        return []
        
    filtered = entries
    if category and category != "All":
        filtered = [e for e in entries if e.get("category") == category]
        
    if query:
        keywords = query.lower().split()
        scored = []
        for e in filtered:
            score = sum(1 for kw in keywords if kw in e["content"].lower())
            scored.append((score, e))
        scored.sort(reverse=True, key=lambda x: x[0])
        return [e["content"] for _, e in scored[:top_k]]
        
    return [e["content"] for e in filtered[-top_k:]]

def get_full_history(user_id: str, category: str = None):
    """Get complete decision history"""
    memory = _load_memory()
    entries = memory.get(user_id, [])
    if category and category != "All":
        return [e for e in entries if e.get("category") == category]
    return entries

def get_decision_count(user_id: str):
    memory = _load_memory()
    return len(memory.get(user_id, []))

def clear_all_memory(user_id: str):
    """Clear memory for a user"""
    memory = _load_memory()
    if user_id in memory:
        memory[user_id] = []
    _save_memory(memory)


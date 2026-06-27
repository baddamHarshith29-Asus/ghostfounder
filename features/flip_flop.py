# ─────────────────────────────────────────────
# FEATURE: DECISION REVERSAL TRACKER (FLIP-FLOP SCORE)
# Tracks strategic consistency over time
# ─────────────────────────────────────────────

import os
import json
from datetime import datetime, timedelta

FLIPFLOP_FILE = "data/flipflop_history.json"

# Category-level reversal detection patterns
# Each pair represents contradictory positions
REVERSAL_PAIRS = [
    {
        "category": "Pricing",
        "position_a": {
            "name": "Value Pricing",
            "keywords": ["no discount", "premium", "raise price", "value", "never compete on price", "high price", "charge more"]
        },
        "position_b": {
            "name": "Discount/Cheap Strategy",
            "keywords": ["discount", "cheaper", "low price", "undercut", "free tier", "freemium", "cut price", "promotion"]
        }
    },
    {
        "category": "Product",
        "position_a": {
            "name": "Focus on Core",
            "keywords": ["focus", "one feature", "core product", "simplify", "remove features", "do less", "single product"]
        },
        "position_b": {
            "name": "Feature Expansion",
            "keywords": ["add features", "new features", "build more", "5 features", "many features", "expand product", "feature list"]
        }
    },
    {
        "category": "Growth",
        "position_a": {
            "name": "Bootstrap / Lean",
            "keywords": ["bootstrap", "lean", "profitable", "organic growth", "sustainable", "slow growth", "self-funded"]
        },
        "position_b": {
            "name": "Aggressive Scaling",
            "keywords": ["raise funding", "scale fast", "grow fast", "hire aggressively", "vc", "venture capital", "blitzscale"]
        }
    },
    {
        "category": "Team",
        "position_a": {
            "name": "Stay Small",
            "keywords": ["small team", "lean team", "no hiring", "do it ourselves", "solo", "contractors"]
        },
        "position_b": {
            "name": "Hire Aggressively",
            "keywords": ["hire", "recruit", "expand team", "3 engineers", "5 people", "build team", "full-time"]
        }
    },
    {
        "category": "Market",
        "position_a": {
            "name": "Niche Focus",
            "keywords": ["niche", "narrow market", "specific audience", "vertical", "one segment", "target market"]
        },
        "position_b": {
            "name": "Go Broad",
            "keywords": ["everyone", "all customers", "mass market", "horizontal", "broad audience", "all segments"]
        }
    }
]


def _load_flipflop_history():
    if os.path.exists(FLIPFLOP_FILE):
        try:
            with open(FLIPFLOP_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def _save_flipflop_history(data):
    os.makedirs("data", exist_ok=True)
    with open(FLIPFLOP_FILE, "w") as f:
        json.dump(data, f, indent=2)

def _detect_position(message: str) -> list:
    """Detect which positions a message aligns with."""
    message_lower = message.lower()
    positions = []
    
    for pair in REVERSAL_PAIRS:
        a_matches = sum(1 for kw in pair["position_a"]["keywords"] if kw in message_lower)
        b_matches = sum(1 for kw in pair["position_b"]["keywords"] if kw in message_lower)
        
        if a_matches > 0 and a_matches > b_matches:
            positions.append({
                "category": pair["category"],
                "position": "A",
                "positionName": pair["position_a"]["name"],
                "strength": a_matches
            })
        elif b_matches > 0 and b_matches > a_matches:
            positions.append({
                "category": pair["category"],
                "position": "B",
                "positionName": pair["position_b"]["name"],
                "strength": b_matches
            })
    
    return positions

def record_positions(user_id: str, message: str):
    """Record detected positions from a message."""
    positions = _detect_position(message)
    
    if not positions:
        return
    
    history = _load_flipflop_history()
    if user_id not in history:
        history[user_id] = {
            "positions": [],
            "reversals": [],
            "lastReversalDate": None
        }
    
    user_data = history[user_id]
    timestamp = datetime.now().isoformat()
    
    for pos in positions:
        # Check if this contradicts a previous position in the same category
        prev_positions = [p for p in user_data["positions"] if p["category"] == pos["category"]]
        
        if prev_positions:
            last_pos = prev_positions[-1]
            if last_pos["position"] != pos["position"]:
                # REVERSAL DETECTED
                user_data["reversals"].append({
                    "category": pos["category"],
                    "from": last_pos["positionName"],
                    "to": pos["positionName"],
                    "timestamp": timestamp,
                    "messagePreview": message[:80] + "..." if len(message) > 80 else message
                })
                user_data["lastReversalDate"] = timestamp
        
        # Record this position
        user_data["positions"].append({
            "category": pos["category"],
            "position": pos["position"],
            "positionName": pos["positionName"],
            "strength": pos["strength"],
            "timestamp": timestamp
        })
    
    # Keep last 100 position records
    if len(user_data["positions"]) > 100:
        user_data["positions"] = user_data["positions"][-100:]
    
    history[user_id] = user_data
    _save_flipflop_history(history)

def get_flipflop_score(user_id: str) -> dict:
    """
    Calculate the strategic consistency score.
    Returns score, reversals, streak, and category breakdown.
    """
    history = _load_flipflop_history()
    user_data = history.get(user_id, {
        "positions": [],
        "reversals": [],
        "lastReversalDate": None
    })
    
    reversals = user_data.get("reversals", [])
    positions = user_data.get("positions", [])
    last_reversal_date = user_data.get("lastReversalDate")
    
    # Calculate consistency score (starts at 100, loses points per reversal)
    base_score = 100
    penalty_per_reversal = 12
    score = max(0, base_score - (len(reversals) * penalty_per_reversal))
    
    # Calculate commitment streak (days since last reversal)
    streak_days = 0
    if last_reversal_date:
        try:
            last_dt = datetime.fromisoformat(last_reversal_date)
            streak_days = (datetime.now() - last_dt).days
        except Exception:
            streak_days = 0
    elif positions:
        # Never reversed — streak is from first position
        try:
            first_dt = datetime.fromisoformat(positions[0]["timestamp"])
            streak_days = (datetime.now() - first_dt).days
        except Exception:
            streak_days = 0
    
    # Category breakdown
    categories = {}
    for pair in REVERSAL_PAIRS:
        cat = pair["category"]
        cat_reversals = [r for r in reversals if r["category"] == cat]
        cat_positions = [p for p in positions if p["category"] == cat]
        
        if cat_positions:
            latest = cat_positions[-1]
            categories[cat] = {
                "currentPosition": latest["positionName"],
                "reversalCount": len(cat_reversals),
                "isConsistent": len(cat_reversals) == 0,
                "status": "consistent" if len(cat_reversals) == 0 else "warning" if len(cat_reversals) == 1 else "critical"
            }
        else:
            categories[cat] = {
                "currentPosition": "Not established",
                "reversalCount": 0,
                "isConsistent": True,
                "status": "neutral"
            }
    
    # Determine overall grade
    if score >= 85:
        grade = "A"
        gradeLabel = "Rock Solid"
        gradeColor = "#10b981"
    elif score >= 70:
        grade = "B"
        gradeLabel = "Mostly Consistent"
        gradeColor = "#6366f1"
    elif score >= 50:
        grade = "C"
        gradeLabel = "Wavering"
        gradeColor = "#f59e0b"
    elif score >= 30:
        grade = "D"
        gradeLabel = "Flip-Flopping"
        gradeColor = "#f97316"
    else:
        grade = "F"
        gradeLabel = "Strategic Chaos"
        gradeColor = "#ef4444"
    
    return {
        "score": score,
        "grade": grade,
        "gradeLabel": gradeLabel,
        "gradeColor": gradeColor,
        "totalReversals": len(reversals),
        "recentReversals": reversals[-5:] if reversals else [],
        "streakDays": streak_days,
        "categories": categories,
        "totalPositions": len(positions)
    }

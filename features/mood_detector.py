# ─────────────────────────────────────────────
# FEATURE: FOUNDER MOOD & BURNOUT DETECTOR
# Analyzes emotional tone of founder messages
# ─────────────────────────────────────────────

import os
import json
import time
from datetime import datetime

MOOD_FILE = "data/mood_history.json"

# ── Sentiment Word Banks ─────────────────────

PANIC_WORDS = [
    "urgent", "emergency", "dying", "bleeding", "crash", "disaster", "panic",
    "desperate", "help", "asap", "immediately", "catastrophe", "failing",
    "collapsing", "screwed", "doomed", "nightmare", "crisis", "sos", "broke",
    "bankrupt", "losing", "lost everything", "can't sleep", "anxiety", "stressed",
    "overwhelmed", "drowning", "burning out", "exhausted", "terrified"
]

OVERCONFIDENCE_WORDS = [
    "definitely", "guaranteed", "easy", "obvious", "no way we fail", "unstoppable",
    "dominate", "crush", "destroy", "monopoly", "billions", "unicorn", "viral",
    "10x", "100x", "moon", "rocket", "inevitable", "no competition", "everyone wants",
    "this will be huge", "can't lose", "next facebook", "next uber", "disrupt"
]

FATIGUE_WORDS = [
    "tired", "exhausted", "burnt out", "burnout", "overwhelmed", "can't focus",
    "too much", "overloaded", "drowning", "no sleep", "working nonstop", "18 hours",
    "haven't stopped", "need a break", "running on fumes", "depleted", "drained",
    "scattered", "unfocused", "confused", "lost track", "forgot", "brain fog"
]

DESPERATION_WORDS = [
    "anything", "whatever it takes", "last chance", "hail mary", "only option",
    "no choice", "backed into a corner", "do or die", "all in", "bet everything",
    "last resort", "running out of time", "running out of money", "can't afford",
    "begging", "please help", "don't know what to do", "giving up", "shutting down"
]

CALM_WORDS = [
    "let's think", "analyze", "consider", "evaluate", "research", "data",
    "metrics", "hypothesis", "test", "experiment", "iterate", "plan",
    "strategy", "review", "assess", "measured", "careful", "thoughtful",
    "patient", "step by step", "methodical", "systematic"
]

EXCITEMENT_WORDS = [
    "excited", "amazing", "awesome", "great news", "breakthrough", "milestone",
    "shipped", "launched", "growing", "traction", "customers love", "positive",
    "momentum", "winning", "progress", "proud", "celebration", "nailed it"
]

# ── Mood Categories ──────────────────────────

MOOD_STATES = {
    "calm": {"label": "😌 Calm & Focused", "color": "#10b981", "advice": "Great headspace. This is when your best decisions happen."},
    "excited": {"label": "🚀 Excited & Energized", "color": "#6366f1", "advice": "Channel this energy wisely. Excitement can lead to over-commitment."},
    "anxious": {"label": "😰 Anxious & Stressed", "color": "#f59e0b", "advice": "Pause before making decisions. Anxiety leads to reactive choices."},
    "panic": {"label": "🔥 Panic Mode", "color": "#ef4444", "advice": "STOP. Do not make major decisions right now. Take 24 hours before committing to anything."},
    "overconfident": {"label": "⚡ Overconfident", "color": "#f97316", "advice": "Dangerous territory. This is where blind spots form. Ask: what am I not seeing?"},
    "fatigued": {"label": "😴 Burnout Risk", "color": "#ec4899", "advice": "Your judgment is compromised when you're exhausted. Delegate or rest before deciding."},
    "desperate": {"label": "🆘 Desperation Detected", "color": "#dc2626", "advice": "Desperation leads to bad deals, bad hires, and bad pivots. Call a mentor first."},
}

def _load_mood_history():
    if os.path.exists(MOOD_FILE):
        try:
            with open(MOOD_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def _save_mood_history(data):
    os.makedirs("data", exist_ok=True)
    with open(MOOD_FILE, "w") as f:
        json.dump(data, f, indent=2)

def _count_matches(text, word_list):
    """Count how many sentiment words from a list appear in the text."""
    text_lower = text.lower()
    count = 0
    for word in word_list:
        if word in text_lower:
            count += 1
    return count

def analyze_mood(message: str) -> dict:
    """
    Analyze the emotional tone of a single message.
    Returns mood state, scores, and advice.
    """
    scores = {
        "panic": _count_matches(message, PANIC_WORDS),
        "overconfidence": _count_matches(message, OVERCONFIDENCE_WORDS),
        "fatigue": _count_matches(message, FATIGUE_WORDS),
        "desperation": _count_matches(message, DESPERATION_WORDS),
        "calm": _count_matches(message, CALM_WORDS),
        "excitement": _count_matches(message, EXCITEMENT_WORDS),
    }
    
    # Determine dominant mood
    max_score = max(scores.values())
    
    if max_score == 0:
        # No strong signal — default to calm
        dominant = "calm"
    else:
        # Map score keys to mood state keys
        score_to_mood = {
            "panic": "panic",
            "overconfidence": "overconfident",
            "fatigue": "fatigued",
            "desperation": "desperate",
            "calm": "calm",
            "excitement": "excited"
        }
        dominant_key = max(scores, key=scores.get)
        dominant = score_to_mood[dominant_key]
    
    # Calculate an overall "stability" score (0-100)
    # High calm/excitement = high stability, high panic/desperation = low stability
    positive = scores["calm"] * 15 + scores["excitement"] * 10
    negative = scores["panic"] * 20 + scores["desperation"] * 18 + scores["fatigue"] * 12 + scores["overconfidence"] * 8
    
    raw_stability = 70 + positive - negative
    stability_score = max(0, min(100, raw_stability))
    
    mood_info = MOOD_STATES[dominant]
    
    return {
        "mood": dominant,
        "label": mood_info["label"],
        "color": mood_info["color"],
        "advice": mood_info["advice"],
        "stabilityScore": stability_score,
        "scores": scores,
        "isWarning": dominant in ["panic", "desperate", "fatigued"],
        "isCritical": dominant in ["panic", "desperate"]
    }

def record_mood(user_id: str, message: str) -> dict:
    """
    Analyze mood and record it to history for timeline tracking.
    Returns the mood analysis result.
    """
    analysis = analyze_mood(message)
    
    history = _load_mood_history()
    if user_id not in history:
        history[user_id] = []
    
    entry = {
        "timestamp": datetime.now().isoformat(),
        "mood": analysis["mood"],
        "label": analysis["label"],
        "stabilityScore": analysis["stabilityScore"],
        "messagePreview": message[:80] + "..." if len(message) > 80 else message
    }
    history[user_id].append(entry)
    
    # Keep last 50 entries per user
    if len(history[user_id]) > 50:
        history[user_id] = history[user_id][-50:]
    
    _save_mood_history(history)
    return analysis

def get_mood_timeline(user_id: str) -> dict:
    """
    Get mood history timeline for visualization.
    Returns timeline entries and aggregate stats.
    """
    history = _load_mood_history()
    entries = history.get(user_id, [])
    
    if not entries:
        return {
            "entries": [],
            "currentMood": MOOD_STATES["calm"],
            "currentMoodKey": "calm",
            "averageStability": 70,
            "warningCount": 0,
            "totalEntries": 0
        }
    
    # Calculate aggregate statistics
    total_stability = sum(e["stabilityScore"] for e in entries)
    avg_stability = round(total_stability / len(entries))
    warning_count = sum(1 for e in entries if e["mood"] in ["panic", "desperate", "fatigued"])
    
    latest = entries[-1]
    current_mood_key = latest["mood"]
    current_mood = MOOD_STATES.get(current_mood_key, MOOD_STATES["calm"])
    
    return {
        "entries": entries[-20:],  # Last 20 for timeline chart
        "currentMood": current_mood,
        "currentMoodKey": current_mood_key,
        "averageStability": avg_stability,
        "warningCount": warning_count,
        "totalEntries": len(entries)
    }

def get_mood_warning(user_id: str) -> str:
    """
    Check if the founder needs a proactive warning based on recent mood patterns.
    Returns a warning message or None.
    """
    history = _load_mood_history()
    entries = history.get(user_id, [])
    
    if len(entries) < 3:
        return None
    
    recent = entries[-5:]  # Last 5 messages
    
    # Check for sustained panic
    panic_count = sum(1 for e in recent if e["mood"] in ["panic", "desperate"])
    if panic_count >= 3:
        return "⚠️ I've noticed sustained panic in your recent messages. You've been in crisis mode for your last {} messages. Major decisions should wait until you've had a clear-headed conversation with a mentor or advisor.".format(panic_count)
    
    # Check for burnout pattern
    fatigue_count = sum(1 for e in recent if e["mood"] == "fatigued")
    if fatigue_count >= 2:
        return "😴 Burnout warning: Your recent messages show signs of exhaustion. Taking a 24-hour break from strategic decisions is not weakness — it's wisdom."
    
    # Check for overconfidence streak
    overconf_count = sum(1 for e in recent if e["mood"] == "overconfident")
    if overconf_count >= 3:
        return "⚡ Overconfidence alert: You've been unusually bullish in your last few messages. This is often when founders miss critical risks. Play devil's advocate with yourself."
    
    # Check for rapid mood swings
    if len(recent) >= 4:
        moods = [e["mood"] for e in recent[-4:]]
        unique_moods = len(set(moods))
        if unique_moods >= 3:
            return "🔄 Emotional volatility detected: Your mood has shifted {} times in your last 4 messages. Inconsistent emotional state leads to inconsistent strategy. Ground yourself before deciding.".format(unique_moods)
    
    return None

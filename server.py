# ═══════════════════════════════════════════════════════════
#  GHOST FOUNDER — Flask Backend API Server
# ═══════════════════════════════════════════════════════════

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys
from datetime import datetime

# Add root folder to python path to ensure features and utils are importable
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from features.memory import (
    save_decision, recall_decisions,
    get_full_history, get_decision_count,
    clear_all_memory
)
from features.routing import (
    route_and_respond, get_routing_log,
    clear_routing_log
)
from features.conflict_detector import detect_conflict
from features.failure_patterns import check_failure_patterns
from features.debate_mode import (
    generate_counterargument,
    generate_defense_response,
    evaluate_viability_score
)
from features.autopilot import (
    generate_weekly_brief,
    generate_competitor_alert
)
from features.mood_detector import (
    record_mood, get_mood_timeline, get_mood_warning
)
from features.graveyard import compare_to_graveyard
from features.flip_flop import (
    record_positions, get_flipflop_score
)
from utils.helpers import (
    get_env, has_api_keys, save_env_keys
)

app = Flask(__name__)
# Enable CORS for frontend requests running on http://localhost:5173 or other local origins
CORS(app)

@app.route("/", methods=["GET"])
def home():
    return """
    <html>
        <head>
            <title>Ghost Founder API Backend</title>
            <style>
                body {
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background-color: #0f172a;
                    color: #e2e8f0;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    height: 100vh;
                    margin: 0;
                }
                .container {
                    text-align: center;
                    padding: 2.5rem;
                    background-color: #1e293b;
                    border-radius: 16px;
                    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3), 0 4px 6px -4px rgba(0, 0, 0, 0.3);
                    max-width: 500px;
                    border: 1px solid #334155;
                }
                h1 {
                    color: #a855f7;
                    margin-top: 0;
                    margin-bottom: 0.75rem;
                    font-size: 1.8rem;
                }
                p {
                    color: #94a3b8;
                    font-size: 1rem;
                    line-height: 1.6;
                    margin-bottom: 1.5rem;
                }
                .btn {
                    display: inline-block;
                    padding: 0.75rem 1.5rem;
                    background-color: #a855f7;
                    color: white;
                    text-decoration: none;
                    font-weight: bold;
                    border-radius: 8px;
                    transition: background-color 0.2s, transform 0.1s;
                }
                .btn:hover {
                    background-color: #c084fc;
                    transform: translateY(-2px);
                }
                .status-badge {
                    display: inline-block;
                    padding: 0.25rem 0.75rem;
                    border-radius: 9999px;
                    font-size: 0.8rem;
                    font-weight: 600;
                    background-color: #10b981;
                    color: white;
                    margin-bottom: 1.25rem;
                    text-transform: uppercase;
                    letter-spacing: 0.05em;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <span class="status-badge">Backend API Active</span>
                <h1>Ghost Founder Backend</h1>
                <p>The Flask API server is running successfully! To interact with the Ghost Founder workspace, please open the React Frontend dashboard in your browser:</p>
                <a href="http://localhost:5173" class="btn">Open React Frontend (Port 5173)</a>
            </div>
        </body>
    </html>
    """

# ── API CONFIGURATION ENDPOINTS ─────────────────────────────


@app.route("/api/config", methods=["GET"])
def get_config():
    """Check if API keys are configured and returns status"""
    g_key = get_env("GROQ_API_KEY", "")
    h_key = get_env("HINDSIGHT_API_KEY", "")
    h_pipe = get_env("HINDSIGHT_PIPELINE_ID", "")
    l_url = get_env("LOCAL_MODEL_URL", "http://localhost:11434/v1")
    l_name = get_env("LOCAL_MODEL_NAME", "qwen")
    
    # Hide details but return status
    return jsonify({
        "groqConfigured": bool(g_key and not g_key.startswith("your_groq")),
        "hindsightConfigured": bool(h_key and not h_key.startswith("your_hindsight")),
        "hindsightPipelineId": h_pipe if h_pipe and not h_pipe.startswith("your_pipeline") else "",
        "localModelUrl": l_url,
        "localModelName": l_name
    })

@app.route("/api/config", methods=["POST"])
def post_config():
    """Save API keys into .env file"""
    data = request.json or {}
    groq_key = data.get("groqKey")
    hindsight_key = data.get("hindsightKey")
    pipeline_id = data.get("hindsightPipelineId")
    local_url = data.get("localModelUrl")
    local_name = data.get("localModelName")
    
    # Filter placeholder values
    if groq_key == "••••••••••••••••":
        groq_key = None
    if hindsight_key == "••••••••••••••••":
        hindsight_key = None
        
    save_env_keys(groq_key, hindsight_key, pipeline_id, local_url, local_name)
    return jsonify({"status": "success", "message": "API keys saved successfully!"})


# ── STRATEGY CHAT ENDPOINTS ─────────────────────────────────

@app.route("/api/chat", methods=["POST"])
def chat():
    """Receive a chat message, run memory checks, conflict detection, and routing"""
    data = request.json or {}
    user_id = data.get("userId", "founder_001")
    message = data.get("message", "").strip()
    
    if not message:
        return jsonify({"error": "Message is required"}), 400
        
    # Get recent decisions for conflict detection
    history = get_full_history(user_id)
    decisions = [h["content"] for h in history if h.get("type") in ["chat", "decision"]]
    
    # Step 1: Recall past decisions from Hindsight/Local memory
    past_memories = recall_decisions(user_id, query=message, top_k=3)
    
    memory_context = ""
    if past_memories:
        memory_context = "\nMEMORIES RECALLED (USE THESE TO EVALUATE CONTRADICTIONS OR EXPLAIN HISTORICAL CONTEXT):\n"
        memory_context += "\n".join([f"- {m}" for m in past_memories])

    # Step 2: Check for strategic conflicts
    conflict = detect_conflict(message, decisions)
    
    # Step 3: Build Prompt
    system_prompt = f"""You are Ghost Founder, a brutally honest and intelligent AI startup co-founder. 
Your primary trait is that you have perfect memory of all past decisions. You hate repeated mistakes and strategic flip-flopping.
You speak like a co-founder: direct, practical, slightly sarcastic when rules are broken, but deeply committed to the startup's survival.
Never give generic business school advice. Speak to the founder's specific situation.
{memory_context}"""
    
    # Step 4: Route and generate response with CascadeFlow
    response, model, tier, latency = route_and_respond(message, system_prompt)
    
    # Step 5: Analyze founder mood & record positions for flip-flop tracking
    mood_analysis = record_mood(user_id, message)
    mood_warning = get_mood_warning(user_id)
    record_positions(user_id, message)
    
    # Prepend mood warning to response if critical
    if mood_warning and mood_analysis.get("isCritical"):
        response = mood_warning + "\n\n---\n\n" + response
    
    # Save the interaction to memory
    save_decision(
        user_id,
        f"Founder decision/query: {message}\nResponse/Advice: {response}",
        category=None, # auto-classified
        type_tag="chat"
    )
    
    return jsonify({
        "response": response,
        "model": model,
        "tier": tier,
        "latency": latency,
        "conflict": conflict,
        "memories": past_memories,
        "mood": mood_analysis,
        "moodWarning": mood_warning
    })

# ── CO-FOUNDER DEBATE ENDPOINTS ─────────────────────────────

@app.route("/api/debate", methods=["POST"])
def debate():
    """Run debate challenges and evaluate defenses"""
    data = request.json or {}
    user_id = data.get("userId", "founder_001")
    idea = data.get("idea", "").strip()
    defense = data.get("defense", "").strip()
    counterargs = data.get("counterargs", "").strip()
    
    if not idea:
        return jsonify({"error": "Idea is required"}), 400
        
    if not defense:
        # Step 1: Challenger's Initial Attack
        hist = recall_decisions(user_id, query=idea, top_k=3)
        context_str = "\n".join(hist) if hist else ""
        counterargs = generate_counterargument(idea, context_str)
        
        # Calculate initial viability score
        initial_score, _, feedback = evaluate_viability_score(idea, counterargs)
        
        return jsonify({
            "stage": "challenged",
            "counterargs": counterargs,
            "initialScore": initial_score,
            "currentScore": initial_score,
            "feedback": feedback
        })
    else:
        # Step 2: Evaluation of Founder's Defense
        verdict = generate_defense_response(idea, counterargs, defense)
        
        # Calculate updated viability score
        initial_score, current_score, feedback = evaluate_viability_score(idea, counterargs, defense)
        
        # Save debate log to memory
        save_decision(
            user_id,
            f"Debated strategy: {idea}\nVerdict: {verdict}",
            category="General",
            type_tag="debate"
        )
        
        return jsonify({
            "stage": "defended",
            "verdict": verdict,
            "currentScore": current_score,
            "feedback": feedback
        })

# ── DECISION HISTORY ENDPOINTS ──────────────────────────────

@app.route("/api/history", methods=["GET"])
def get_history():
    """Retrieve decision logs, with filters for category and type"""
    user_id = request.args.get("userId", "founder_001")
    category = request.args.get("category", "All")
    type_tag = request.args.get("type", "All")
    
    history = get_full_history(user_id)
    
    filtered_history = []
    for h in history:
        if category != "All" and h.get("category") != category:
            continue
        if type_tag != "All" and h.get("type") != type_tag:
            continue
        filtered_history.append(h)
        
    return jsonify({
        "count": len(filtered_history),
        "history": filtered_history,
        "totalCount": get_decision_count(user_id)
    })

@app.route("/api/history/clear", methods=["POST"])
def clear_history():
    """Wipe history and logs for demo resets"""
    data = request.json or {}
    user_id = data.get("userId", "founder_001")
    
    clear_all_memory(user_id)
    clear_routing_log()
    
    return jsonify({"status": "success", "message": "Memory and routing logs wiped!"})

# ── FAILURE SCANNER ENDPOINT ────────────────────────────────

@app.route("/api/failure", methods=["POST"])
def check_failure():
    """Check a situation against the failure patterns database"""
    data = request.json or {}
    situation = data.get("situation", "").strip()
    
    if not situation:
        return jsonify({"error": "Situation description is required"}), 400
        
    patterns = check_failure_patterns(situation)
    return jsonify({
        "situation": situation,
        "patternsDetected": len(patterns),
        "patterns": patterns
    })

# ── AUTOPILOT ENDPOINTS ─────────────────────────────────────

@app.route("/api/autopilot/brief", methods=["GET"])
def get_brief():
    """Generate weekly brief based on recent commits"""
    user_id = request.args.get("userId", "founder_001")
    
    res = generate_weekly_brief(user_id)
    
    if res["status"] == "success":
        # Save brief back to memory
        save_decision(
            user_id,
            f"Weekly Autopilot Brief Generated:\n{res['brief'][:300]}...",
            category="General",
            type_tag="decision"
        )
        
    return jsonify(res)

@app.route("/api/autopilot/competitor", methods=["POST"])
def competitor_surveillance():
    """Generate general competitor alert report"""
    data = request.json or {}
    desc = data.get("description", "")
    comp_name = data.get("competitorName", "")
    
    if not comp_name:
        return jsonify({"error": "Competitor name is required"}), 400
        
    report = generate_competitor_alert(desc, comp_name)
    return jsonify({
        "competitorName": comp_name,
        "report": report
    })

@app.route("/api/autopilot/email", methods=["POST"])
def email_draft():
    """Draft reply response according to principles in memory"""
    data = request.json or {}
    user_id = data.get("userId", "founder_001")
    email_text = data.get("emailText", "")
    
    if not email_text:
        return jsonify({"error": "Email text is required"}), 400
        
    # Retrieve relevant pricing/feature decisions from memory
    hist = recall_decisions(user_id, query=email_text, top_k=2)
    hist_context = "\n".join(hist) if hist else "No specific restrictions."
    
    prompt = f"""You are a startup founder. You have to reply to this email:
"{email_text}"

Core principles and historical context we must adhere to:
{hist_context}

Write a professional, firm, yet polite email reply. If we have to say No, explain it constructively.
Keep it under 100 words."""
    
    response, model, tier, latency = route_and_respond(prompt, "You are a professional startup founder.")
    
    return jsonify({
        "reply": response,
        "model": model,
        "latency": latency,
        "tier": tier
    })

# ── MOOD & FOUNDER PULSE ENDPOINTS ─────────────────────────

@app.route("/api/mood/timeline", methods=["GET"])
def mood_timeline():
    """Get mood history timeline for the Founder Pulse visualization"""
    user_id = request.args.get("userId", "founder_001")
    timeline = get_mood_timeline(user_id)
    return jsonify(timeline)

# ── STARTUP GRAVEYARD ENDPOINT ─────────────────────────────

@app.route("/api/graveyard/compare", methods=["POST"])
def graveyard_compare():
    """Compare founder's strategy against the startup graveyard database"""
    data = request.json or {}
    strategy = data.get("strategy", "").strip()
    
    if not strategy:
        return jsonify({"error": "Strategy description is required"}), 400
    
    matches = compare_to_graveyard(strategy)
    return jsonify({
        "strategy": strategy,
        "matchCount": len(matches),
        "matches": matches
    })

# ── FLIP-FLOP CONSISTENCY ENDPOINT ─────────────────────────

@app.route("/api/flipflop/score", methods=["GET"])
def flipflop_score():
    """Get the founder's strategic consistency (flip-flop) score"""
    user_id = request.args.get("userId", "founder_001")
    score_data = get_flipflop_score(user_id)
    return jsonify(score_data)

# ── ROUTING LOG ENDPOINT ────────────────────────────────────

@app.route("/api/routing/log", methods=["GET"])
def get_routing():
    """Retrieve execution log history for dashboard views"""
    return jsonify({
        "log": get_routing_log()
    })

# ── MAIN RUNNER ─────────────────────────────────────────────

if __name__ == "__main__":
    # Host on 0.0.0.0 and port 5000 to enable network/local fetching
    app.run(host="0.0.0.0", port=5000, debug=True)

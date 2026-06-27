# ═══════════════════════════════════════════════════════════
#  GHOST FOUNDER — AI Co-Founder with Permanent Memory
#  Built with Hindsight (memory) + cascadeflow (routing)
# ═══════════════════════════════════════════════════════════

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import time

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
from utils.helpers import (
    get_env, has_api_keys, save_env_keys
)

# ── Page Config ─────────────────────────────────────────────
st.set_page_config(
    page_title="Ghost Founder | AI Co-Founder",
    page_icon="👻",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Premium Theme CSS ─────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    
    /* Global Styles */
    html, body, [class*="css"], .stApp {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        background-color: #0b0b0f !important;
        color: #e2e8f0 !important;
    }
    
    /* Header styling */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-weight: 700 !important;
        letter-spacing: -0.02em;
        background: linear-gradient(135deg, #ffffff 30%, #a78bfa 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Premium Glassmorphic Cards */
    .glass-card {
        background: rgba(23, 23, 33, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
    }
    
    .glass-card-mini {
        background: rgba(23, 23, 33, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.03);
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
    }
    
    /* Badges & Indicators */
    .badge-purple {
        background: linear-gradient(135deg, #7c3aed 0%, #4c1d95 100%);
        color: #f5f3ff;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 11px;
        font-weight: 600;
        display: inline-block;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .badge-green {
        background: linear-gradient(135deg, #059669 0%, #064e3b 100%);
        color: #ecfdf5;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 11px;
        font-weight: 600;
        display: inline-block;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .badge-amber {
        background: linear-gradient(135deg, #d97706 0%, #78350f 100%);
        color: #fffbeb;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 11px;
        font-weight: 600;
        display: inline-block;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Custom Alerts */
    .conflict-card {
        background: rgba(244, 63, 94, 0.07);
        border: 1px solid rgba(244, 63, 94, 0.2);
        border-left: 4px solid #f43f5e;
        border-radius: 12px;
        padding: 16px;
        margin: 15px 0;
    }
    
    .memory-card {
        background: rgba(16, 185, 129, 0.06);
        border: 1px solid rgba(16, 185, 129, 0.2);
        border-left: 4px solid #10b981;
        border-radius: 12px;
        padding: 16px;
        margin: 15px 0;
    }
    
    /* Inputs & Text Area overrides */
    .stTextArea textarea, .stTextInput input {
        background-color: #121218 !important;
        border: 1px solid #27273a !important;
        color: #e2e8f0 !important;
        border-radius: 10px !important;
    }
    
    .stTextArea textarea:focus, .stTextInput input:focus {
        border-color: #7c3aed !important;
        box-shadow: 0 0 0 1px #7c3aed !important;
    }
    
    /* Sidebar customization */
    [data-testid="stSidebar"] {
        background-color: #08080c !important;
        border-right: 1px solid #181824;
    }
    
    /* Custom styled buttons */
    .stButton>button {
        background: linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%) !important;
        color: white !important;
        font-weight: 600 !important;
        border-radius: 10px !important;
        border: none !important;
        transition: all 0.2s ease;
        padding: 8px 16px !important;
    }
    
    .stButton>button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 15px rgba(124, 58, 237, 0.4);
    }
    
    /* Quick action buttons style */
    .action-btn {
        background-color: #1a1a24;
        border: 1px solid #2d2d3f;
        border-radius: 8px;
        padding: 10px;
        font-size: 13px;
        cursor: pointer;
        display: inline-block;
        margin: 5px;
        color: #a78bfa;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

# ── Session State Setup ─────────────────────────────────────────────
if "user_id" not in st.session_state:
    st.session_state.user_id = "founder_001"
if "messages" not in st.session_state:
    st.session_state.messages = []
if "decisions" not in st.session_state:
    st.session_state.decisions = []
if "debate_stage" not in st.session_state:
    st.session_state.debate_stage = "input"
if "counterargs" not in st.session_state:
    st.session_state.counterargs = ""
if "debate_idea" not in st.session_state:
    st.session_state.debate_idea = ""
if "debate_defense" not in st.session_state:
    st.session_state.debate_defense = ""
if "debate_feedback" not in st.session_state:
    st.session_state.debate_feedback = ""
if "debate_current_score" not in st.session_state:
    st.session_state.debate_current_score = 65
if "debate_initial_score" not in st.session_state:
    st.session_state.debate_initial_score = 65

# Load existing decisions list from memory to keep session state in sync
existing_history = get_full_history(st.session_state.user_id)
if existing_history and not st.session_state.decisions:
    st.session_state.decisions = [h["content"] for h in existing_history]

# ── Sidebar ────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 👻 GHOST FOUNDER")
    st.markdown("<p style='color:#a78bfa; font-style:italic; font-size:13px; margin-top:-10px;'>The Co-Founder that never forgets</p>", unsafe_allow_html=True)
    
    # Decisions Count Badge
    cnt = get_decision_count(st.session_state.user_id)
    st.markdown(f"""
    <div class='glass-card-mini' style='text-align: center;'>
        <p style='margin: 0; font-size: 11px; color: #94a3b8; text-transform: uppercase;'>Decisions Remembered</p>
        <p style='margin: 0; font-size: 32px; font-weight: 800; color: #c084fc;'>{cnt}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Mode Selector
    mode = st.radio(
        "Navigation",
        [
            "💬 Strategy Chat",
            "⚔️ Co-Founder Debate",
            "📊 Decision History",
            "⚠️ Failure Patterns",
            "🤖 Autopilot Suite",
            "⚡ Routing Dashboard"
        ]
    )
    
    st.markdown("---")
    
    # Live API Config Panel
    with st.expander("⚙️ API Configuration"):
        g_key = get_env("GROQ_API_KEY", "")
        h_key = get_env("HINDSIGHT_API_KEY", "")
        h_pipe = get_env("HINDSIGHT_PIPELINE_ID", "")
        
        # Obfuscate existing keys
        groq_disp = "••••••••••••••••" if g_key and not g_key.startswith("your_groq") else ""
        hindsight_disp = "••••••••••••••••" if h_key and not h_key.startswith("your_hindsight") else ""
        pipe_disp = h_pipe if h_pipe and not h_pipe.startswith("your_pipeline") else ""
        
        st.caption("Leave fields blank to use offline simulation mode.")
        new_groq = st.text_input("Groq API Key", value=groq_disp, type="password")
        new_hindsight = st.text_input("Hindsight API Key", value=hindsight_disp, type="password")
        new_pipe = st.text_input("Hindsight Pipeline ID", value=pipe_disp)
        
        if st.button("Save API Configuration", use_container_width=True):
            # Only save if values actually changed
            save_groq = new_groq if new_groq != "••••••••••••••••" else g_key
            save_hindsight = new_hindsight if new_hindsight != "••••••••••••••••" else h_key
            save_p = new_pipe
            
            save_env_keys(save_groq, save_hindsight, save_p)
            st.success("API keys updated!")
            time.sleep(1)
            st.rerun()

    st.markdown("---")
    
    # Reset Buttons
    col_reset_mem, col_reset_route = st.columns(2)
    with col_reset_mem:
        if st.button("🧹 Reset Memory", use_container_width=True):
            clear_all_memory(st.session_state.user_id)
            st.session_state.decisions = []
            st.session_state.messages = []
            st.success("Memory cleared!")
            time.sleep(1)
            st.rerun()
    with col_reset_route:
        if st.button("⚡ Reset Logs", use_container_width=True):
            clear_routing_log()
            st.success("Routing logs cleared!")
            time.sleep(1)
            st.rerun()

    st.markdown("<p style='font-size:11px; text-align:center; color:#475569; margin-top:20px;'>Built with Hindsight + cascadeflow</p>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
#  MODE 1: STRATEGY CHAT
# ══════════════════════════════════════════════════════════
if mode == "💬 Strategy Chat":
    st.markdown("<h1>💬 Strategy Chat</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#94a3b8; margin-top:-10px;'>Ask strategy questions. Ghost Founder retrieves context, watches for contradictions, and routes queries dynamically.</p>", unsafe_allow_html=True)
    
    # Memory Activation Status Banner
    active_keys = has_api_keys()
    if not active_keys:
        st.markdown("""
        <div class='glass-card' style='border: 1px solid rgba(139, 92, 246, 0.3); padding:15px; margin-bottom:15px; background: rgba(139, 92, 246, 0.05);'>
            📢 <strong>Demo Mode Active:</strong> Running with local file memory and simulated co-founder intelligence. Add your Groq API key in the sidebar configuration to unlock live LLM analysis!
        </div>
        """, unsafe_allow_html=True)
        
    # Starter Suggestions / Presets
    st.markdown("##### 🚀 Demo Shortcuts (1-Click Judge Actions)")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🛑 Test Discount Contradiction", use_container_width=True):
            # Seed baseline pricing decision first
            save_decision(
                st.session_state.user_id,
                "On February 14th, I committed that we will never compete on price or run discount campaigns. Discounting attracts transactional customers with high support needs. In January, a price campaign cost us ₹25,000 in refunds and bad reviews.",
                category="Pricing",
                type_tag="decision"
            )
            # Put input in session state to prompt immediately
            st.session_state.chat_shortcut_input = "I'm thinking about running a 50% discount campaign this weekend to quickly boost customer volume. What do you think?"
            st.rerun()
            
    with col2:
        if st.button("🛠️ Test Feature Overload", use_container_width=True):
            save_decision(
                st.session_state.user_id,
                "On March 3rd, we decided to restrict product development. We will focus purely on one core dashboard view and refuse to build additional features until we reach 100 paid users.",
                category="Product",
                type_tag="decision"
            )
            st.session_state.chat_shortcut_input = "Let's build 5 new features this sprint (Slack alerts, custom export, team subaccounts, analytics tab, and calendar sync) so we can appeal to more customers."
            st.rerun()
            
    with col3:
        if st.button("📈 Test Complex Model Routing", use_container_width=True):
            st.session_state.chat_shortcut_input = "Should I seek venture capital funding or bootstrap my startup?"
            st.rerun()

    st.markdown("---")

    # Chat Messages Window
    chat_container = st.container()
    
    with chat_container:
        # If history is empty, show welcoming prompt
        if not st.session_state.messages:
            st.markdown("""
            <div style='text-align: center; padding: 40px; color: #64748b;'>
                👻 <br><strong>Ghost Founder is awake.</strong><br>
                Try saying: <em>"We need to raise $1M next month"</em> or click one of the demo buttons above to see memory recall and conflict warnings fire in real time.
            </div>
            """, unsafe_allow_html=True)
        else:
            for msg in st.session_state.messages:
                role = msg["role"]
                with st.chat_message(role):
                    st.markdown(msg["content"])
                    if role == "assistant" and "model" in msg:
                        badge_color = "badge-green" if "8b" in msg["model"] else "badge-purple"
                        st.markdown(f"""
                        <div style='margin-top: 8px;'>
                            <span class='{badge_color}'>🤖 {msg['model']}</span>
                            <span style='font-size:11px; margin-left:10px; color:#64748b;'>⏱️ {msg.get('latency', 0)}ms | 💸 Cost tier: {msg.get('tier', '')}</span>
                        </div>
                        """, unsafe_allow_html=True)

    # Input handling
    user_input = st.chat_input("Enter strategy query...")
    
    # If click preset, overwrite input
    if "chat_shortcut_input" in st.session_state:
        user_input = st.session_state.chat_shortcut_input
        del st.session_state.chat_shortcut_input

    if user_input:
        # Show user message
        with st.chat_message("user"):
            st.markdown(user_input)
            
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Step 1: Recall past memories semantically
        past_memories = recall_decisions(st.session_state.user_id, query=user_input, top_k=3)
        
        memory_context = ""
        if past_memories:
            memory_context = "\nMEMORIES RECALLED (USE THESE TO EVALUATE CONTRADICTIONS OR EXPLAIN HISTORICAL CONTEXT):\n"
            memory_context += "\n".join([f"- {m}" for m in past_memories])

        # Step 2: Conflict check
        conflict = detect_conflict(user_input, st.session_state.decisions)
        
        # Step 3: Build Prompt
        system_prompt = f"""You are Ghost Founder, a brutally honest and intelligent AI startup co-founder. 
Your primary trait is that you have perfect memory of all past decisions. You hate repeated mistakes and strategic flip-flopping.
You speak like a co-founder: direct, practical, slightly sarcastic when rules are broken, but deeply committed to the startup's survival.
Never give generic business school advice. Speak to the founder's specific situation.
{memory_context}"""
        
        # Step 4: Route with CascadeFlow
        with st.spinner("Ghost Founder is reflecting..."):
            response, model, tier, latency = route_and_respond(user_input, system_prompt)
            
        # Display conflict alerts BEFORE response
        if conflict:
            st.markdown(f"""
            <div class="conflict-card">
                <strong>🚨 STRATEGIC CONTRADICTION DETECTED</strong><br>
                {conflict}
            </div>
            """, unsafe_allow_html=True)
            
        # Display memory utilization indicator
        if past_memories:
            st.markdown(f"""
            <div class="memory-card">
                <strong>🧠 HINDSIGHT MEMORY RETRIEVAL</strong><br>
                Retrieved {len(past_memories)} past decisions/contexts. Factoring these into the strategy.
            </div>
            """, unsafe_allow_html=True)
            
        # Display AI Response
        with st.chat_message("assistant"):
            st.markdown(response)
            badge_color = "badge-green" if "8b" in model else "badge-purple"
            st.markdown(f"""
            <div style='margin-top: 8px;'>
                <span class='{badge_color}'>🤖 {model}</span>
                <span style='font-size:11px; margin-left:10px; color:#64748b;'>⏱️ {latency}ms | 💸 Cost tier: {tier}</span>
            </div>
            """, unsafe_allow_html=True)
            
        # Add to state and save memory
        st.session_state.messages.append({
            "role": "assistant",
            "content": response,
            "model": model,
            "tier": tier,
            "latency": latency
        })
        
        # Save this interaction as a decision memory
        save_decision(
            st.session_state.user_id,
            f"Founder decision/query: {user_input}\nResponse/Advice: {response}",
            category=None, # auto-classified inside features/memory
            type_tag="chat"
        )
        st.session_state.decisions.append(user_input)
        
        # Force redraw to place scroll correctly
        st.rerun()

# ══════════════════════════════════════════════════════════
#  MODE 2: CO-FOUNDER DEBATE
# ══════════════════════════════════════════════════════════
elif mode == "⚔️ Co-Founder Debate":
    st.markdown("<h1>⚔️ Co-Founder Debate Arena</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#94a3b8; margin-top:-10px;'>Pitch an idea. The AI co-founder will stress test it and score your defense. Refine your ideas before pitching to VCs.</p>", unsafe_allow_html=True)
    
    # Presets for quick debate testing
    st.markdown("##### 🥊 Select a Scenario to Debate:")
    col_sc1, col_sc2, col_sc3 = st.columns(3)
    with col_sc1:
        if st.button("📉 Freemium Pricing", use_container_width=True):
            st.session_state.debate_idea = "I want to launch a 100% free tier of our product to drive viral acquisition, hoping they convert later."
            st.session_state.debate_stage = "input"
            st.rerun()
    with col_sc2:
        if st.button("🛠️ Full Rebuild", use_container_width=True):
            st.session_state.debate_idea = "I want to spend 2 months refactoring the database and rebuilding the front-end codebase from scratch to make it faster."
            st.session_state.debate_stage = "input"
            st.rerun()
    with col_sc3:
        if st.button("👥 Fast Hiring", use_container_width=True):
            st.session_state.debate_idea = "I want to hire 3 engineers and 2 sales reps immediately using credit lines to capture market share."
            st.session_state.debate_stage = "input"
            st.rerun()

    st.markdown("---")

    col_arena, col_score = st.columns([3, 2])
    
    with col_arena:
        if st.session_state.debate_stage == "input":
            st.markdown("### 🥊 The Ring: State Your Strategy")
            idea_input = st.text_area(
                "What decision or strategy do you want to defend?",
                value=st.session_state.debate_idea,
                placeholder="Example: I want to introduce a freemium tier to capture email signups...",
                height=150
            )
            
            if st.button("🥊 Challenge Strategy", type="primary", use_container_width=True):
                if idea_input.strip():
                    st.session_state.debate_idea = idea_input
                    
                    # Pull relevant memories to contextualize attack
                    hist = recall_decisions(st.session_state.user_id, query=idea_input, top_k=3)
                    context_str = "\n".join(hist) if hist else ""
                    
                    with st.spinner("Generating counterarguments..."):
                        counterargs = generate_counterargument(idea_input, context_str)
                        
                    st.session_state.counterargs = counterargs
                    st.session_state.debate_stage = "challenge"
                    
                    # Evaluate initial viability score
                    init_score, _, feedback = evaluate_viability_score(idea_input, counterargs)
                    st.session_state.debate_initial_score = init_score
                    st.session_state.debate_current_score = init_score
                    st.session_state.debate_feedback = feedback
                    
                    st.rerun()
                    
        elif st.session_state.debate_stage in ["challenge", "defended"]:
            st.markdown("### 🥊 Challenger's Attack")
            st.markdown(f"**Your Proposed Strategy:** *{st.session_state.debate_idea}*")
            st.error(st.session_state.counterargs)
            st.markdown("---")
            
            if st.session_state.debate_stage == "challenge":
                st.markdown("### 🛡️ Defend Your Idea")
                defense_input = st.text_area(
                    "Explain why this decision is correct despite the risks:",
                    placeholder="We have data showing that free users convert at 5%... We will run a 2-week MVP...",
                    height=120
                )
                
                col_sub1, col_sub2 = st.columns(2)
                with col_sub1:
                    if st.button("🛡️ Defend Strategy", type="primary", use_container_width=True):
                        if defense_input.strip():
                            st.session_state.debate_defense = defense_input
                            with st.spinner("Evaluating defense..."):
                                verdict = generate_defense_response(
                                    st.session_state.debate_idea,
                                    st.session_state.counterargs,
                                    defense_input
                                )
                                # Re-evaluate score
                                init_score, cur_score, feed = evaluate_viability_score(
                                    st.session_state.debate_idea,
                                    st.session_state.counterargs,
                                    defense_input
                                )
                                st.session_state.debate_current_score = cur_score
                                st.session_state.debate_feedback = feed
                                st.session_state.verdict = verdict
                                st.session_state.debate_stage = "defended"
                                
                                # Log outcome to memory
                                save_decision(
                                    st.session_state.user_id,
                                    f"Debated strategy: {st.session_state.debate_idea}\nVerdict: {verdict}",
                                    category="General",
                                    type_tag="debate"
                                )
                                st.rerun()
                with col_sub2:
                    if st.button("🔄 Reset Arena", use_container_width=True):
                        st.session_state.debate_stage = "input"
                        st.session_state.debate_idea = ""
                        st.session_state.counterargs = ""
                        st.session_state.debate_defense = ""
                        st.rerun()
            else:
                st.markdown("### 🛡️ Your Defense")
                st.info(st.session_state.debate_defense)
                st.markdown("### ⚖️ Co-Founder's Final Verdict")
                st.success(st.session_state.verdict)
                
                if st.button("🔄 Start New Debate", use_container_width=True):
                    st.session_state.debate_stage = "input"
                    st.session_state.debate_idea = ""
                    st.session_state.counterargs = ""
                    st.session_state.debate_defense = ""
                    st.rerun()
                    
    with col_score:
        st.markdown("### 📊 Strategy Scorecard")
        if st.session_state.debate_stage == "input":
            st.markdown("""
            <div style='text-align: center; padding: 30px; border: 1px dashed rgba(255,255,255,0.1); border-radius:12px; color:#475569;'>
                Pitch your idea to view the live Idea Viability Index and receive feedback.
            </div>
            """, unsafe_allow_html=True)
        else:
            # Gauge Chart or Bar Chart
            score = st.session_state.debate_current_score
            initial = st.session_state.debate_initial_score
            delta = score - initial
            
            # Format Color based on score
            if score > 75:
                color_hex = "#10b981" # Green
            elif score > 50:
                color_hex = "#f59e0b" # Orange
            else:
                color_hex = "#ef4444" # Red
                
            st.markdown(f"""
            <div class='glass-card' style='text-align: center;'>
                <p style='margin: 0; font-size: 14px; color: #94a3b8;'>IDEA VIABILITY INDEX</p>
                <h1 style='margin: 10px 0; font-size: 64px; background: none; -webkit-text-fill-color: {color_hex};'>{score} <span style='font-size:24px; color:#475569;'>/ 100</span></h1>
                <p style='font-size: 13px; font-weight:600; color: {"#10b981" if delta >= 0 else "#f43f5e"};'>
                    {"▲ Defense improved score by +" + str(delta) if delta > 0 else "▼ Score dropped or remained static: " + str(delta)}
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Show Progress Bar
            st.progress(score / 100)
            
            # Show Feedback Card
            st.markdown(f"""
            <div class='glass-card-mini' style='margin-top: 15px;'>
                <strong>📋 Co-Founder Feedback:</strong><br>
                <p style='font-size:13px; color:#cbd5e1; margin-top:5px;'>{st.session_state.debate_feedback}</p>
            </div>
            """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
#  MODE 3: DECISION HISTORY
# ══════════════════════════════════════════════════════════
elif mode == "📊 Decision History":
    st.markdown("<h1>📊 Decision History</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#94a3b8; margin-top:-10px;'>A chronological record of every decision you have committed to, organized by category.</p>", unsafe_allow_html=True)

    # Filter Toolbar
    cols_filter = st.columns([2, 1, 1])
    with cols_filter[0]:
        search_query = st.text_input("🔍 Search Decisions", placeholder="Search by keywords...")
    with cols_filter[1]:
        filter_cat = st.selectbox("📁 Filter by Category", ["All", "Pricing", "Product", "Marketing", "Finance", "Team", "General"])
    with cols_filter[2]:
        filter_type = st.selectbox("🏷️ Filter by Type", ["All", "decision", "chat", "debate"])

    history = get_full_history(st.session_state.user_id)

    # Filter data in Python
    filtered_history = []
    for h in history:
        # Search match
        if search_query and search_query.lower() not in h["content"].lower():
            continue
        # Category match
        if filter_cat != "All" and h.get("category") != filter_cat:
            continue
        # Type match
        if filter_type != "All" and h.get("type") != filter_type:
            continue
        filtered_history.append(h)

    if not filtered_history:
        st.info("No decision records matching filters. Go type some strategies in the chat!")
    else:
        st.markdown(f"Found **{len(filtered_history)}** decisions.")
        
        # Timeline Chart
        if len(filtered_history) >= 2:
            st.markdown("### Journey Timeline")
            # Build list of points
            dates = []
            for h in filtered_history:
                try:
                    dt = datetime.fromisoformat(h["timestamp"]).strftime("%b %d %H:%M")
                except Exception:
                    dt = h.get("timestamp", "")[:16]
                dates.append(dt)
                
            categories = [h.get("category", "General") for h in filtered_history]
            labels = [h["content"][:40] + "..." for h in filtered_history]
            
            fig = px.scatter(
                x=dates,
                y=categories,
                text=labels,
                color=categories,
                title="Historical Decision Map",
                labels={"x": "Timestamp", "y": "Startup Category"},
                height=300
            )
            fig.update_traces(textposition='top center', marker=dict(size=14, line=dict(width=1, color='white')))
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(23, 23, 33, 0.4)",
                font_color="#e2e8f0",
                showlegend=False,
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor="#1e293b")
            )
            st.plotly_chart(fig, use_container_width=True)

        # Timeline cards
        st.markdown("### Chronological Feed")
        for i, entry in enumerate(reversed(filtered_history)):
            try:
                date_str = datetime.fromisoformat(entry["timestamp"]).strftime("%A, %B %d, %Y at %I:%M %p")
            except Exception:
                date_str = entry.get("timestamp", "")
                
            cat = entry.get("category", "General")
            t_tag = entry.get("type", "decision")
            hindsight_stored = entry.get("hindsight_stored", False)
            
            # Badge styles
            badge_html = f"<span class='badge-purple'>{cat}</span>"
            if cat == "Pricing":
                badge_html = "<span class='badge-amber'>🏷️ Pricing</span>"
            elif cat == "Product":
                badge_html = "<span class='badge-purple'>💻 Product</span>"
            elif cat == "Marketing":
                badge_html = "<span class='badge-green'>📈 Marketing</span>"
            elif cat == "Finance":
                badge_html = "<span class='badge-green'>💰 Finance</span>"
                
            hindsight_badge = "<span style='color:#10b981; font-size:11px; margin-left:10px;'>✓ Saved to Hindsight Pipeline</span>" if hindsight_stored else ""

            st.markdown(f"""
            <div class='glass-card'>
                <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;'>
                    <div>
                        {badge_html}
                        <span style='background:rgba(255,255,255,0.05); color:#94a3b8; font-size:10px; padding:2px 8px; border-radius:5px; margin-left:10px;'>Type: {t_tag}</span>
                        {hindsight_badge}
                    </div>
                    <span style='color:#64748b; font-size:12px;'>{date_str}</span>
                </div>
                <div style='color:#cbd5e1; font-size:14px; white-space: pre-wrap;'>{entry['content']}</div>
            </div>
            """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
#  MODE 4: FAILURE PATTERNS
# ══════════════════════════════════════════════════════════
elif mode == "⚠️  Failure Patterns":
    st.title("⚠️ Failure Pattern Scanner")
    st.markdown("<p style='color:#94a3b8; margin-top:-10px;'>Scan your strategy against a database compiled from 1,000+ real-world startup failures.</p>", unsafe_allow_html=True)
    
    # Scenario Presets
    st.markdown("##### 🚀 Click to Test Common Failure Scenarios:")
    col_p1, col_p2, col_p3 = st.columns(3)
    with col_p1:
        if st.button("🏷️ Price Undercutting Campaign", use_container_width=True):
            st.session_state.fail_text = "We want to launch next week by undercutting our major competitors by 50% and running heavy discounts. We will acquire their users fast."
            st.rerun()
    with col_p2:
        if st.button("💻 Feature-Rich Launch Plan", use_container_width=True):
            st.session_state.fail_text = "We are going to hold the launch for another month so that we can build Slack alerts, dashboard export, sub-accounts, and 5 other features to satisfy every customer."
            st.rerun()
    with col_p3:
        if st.button("💰 Burn Rate Inflation", use_container_width=True):
            st.session_state.fail_text = "We plan to raise our burn rate by hiring 3 developers and renting a workspace before we lock in our retention. We need to grow fast."
            st.rerun()

    st.markdown("---")

    input_val = st.session_state.get("fail_text", "")
    situation = st.text_area(
        "Describe your current strategy or launching plan:",
        value=input_val,
        placeholder="We are preparing to expand to 3 cities, cut prices, and build out a calendar integration...",
        height=150
    )
    
    if st.button("🔍 Scan for Danger Patterns", type="primary", use_container_width=True):
        if situation.strip():
            with st.spinner("Scanning against failure database..."):
                patterns = check_failure_patterns(situation)
                
            if patterns:
                st.markdown(f"### 🚨 Danger Signals Detected ({len(patterns)})")
                for p in patterns:
                    st.markdown(f"""
                    <div class='glass-card' style='border:1px solid rgba(244,63,94,0.3); border-left: 5px solid #f43f5e;'>
                        <div style='display:flex; justify-content:space-between; align-items:center;'>
                            <h4 style='margin:0; background:none; -webkit-text-fill-color:#f43f5e;'>❌ {p['name']}</h4>
                            <span class='badge-amber' style='background:#f43f5e; color:#fff;'>Failure Rate: {p['failure_rate']}</span>
                        </div>
                        <p style='margin-top:10px; font-size:14px;'><strong>The Lesson:</strong> {p['lesson']}</p>
                        <p style='font-size:13px; color:#94a3b8;'><strong>Real-World Examples:</strong></p>
                        <ul style='font-size:13px; color:#cbd5e1; margin-top:-5px;'>
                            {"".join([f"<li>{ex}</li>" for ex in p['examples']])}
                        </ul>
                        <div style='background:rgba(16,185,129,0.08); padding:10px; border-radius:8px; margin-top:10px; border: 1px solid rgba(16,185,129,0.2);'>
                            <span style='color:#10b981; font-weight:700;'>💡 Ghost Founder's Correction:</span> {p['fix']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class='glass-card' style='border:1px solid rgba(16,185,129,0.3); text-align:center;'>
                    <h3 style='color:#10b981; background:none; -webkit-text-fill-color:#10b981;'>✅ No Danger Signals Detected</h3>
                    <p style='margin:0; font-size:14px; color:#cbd5e1;'>Your strategy does not trigger any of our primary startup failure filters. Proceed, but validate unit economics continuously.</p>
                </div>
                """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
#  MODE 5: AUTOPILOT SUITE
# ══════════════════════════════════════════════════════════
elif mode == "🤖 Autopilot Suite":
    st.markdown("<h1>🤖 Startup Autopilot Mode</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#94a3b8; margin-top:-10px;'>While you sleep, Ghost Founder runs simulations, monitors competitors, checks support channels, and drafts morning briefs.</p>", unsafe_allow_html=True)

    tab_brief, tab_comp, tab_email = st.tabs(["📋 Monday Morning Brief", "🛡️ Competitor Watch", "✉️ Support Draft Helper"])

    with tab_brief:
        st.markdown("### Weekly Strategic Assessment")
        st.caption("Ghost Founder synthesizes your entire memory trail into a core strategic direction.")
        
        history = get_full_history(st.session_state.user_id)
        
        if not history:
            st.info("No history found yet. Go chat in Strategy Chat or run a debate to seed decisions.")
        else:
            if st.button("📋 Generate Assessment Brief", type="primary", use_container_width=True):
                with st.spinner("Analyzing recent commits..."):
                    res = generate_weekly_brief(st.session_state.user_id)
                    
                if res["status"] == "success":
                    st.markdown(f"<p style='color:#64748b; font-size:12px;'>Generated at {res['generated_at']} (based on {res['based_on']} historical inputs)</p>", unsafe_allow_html=True)
                    st.markdown("---")
                    st.markdown(res["brief"])
                    st.markdown("---")
                    
                    # Store brief back to memory
                    save_decision(
                        st.session_state.user_id,
                        f"Weekly Autopilot Brief Generated:\n{res['brief'][:300]}...",
                        category="General",
                        type_tag="decision"
                    )
                else:
                    st.error(res.get("message", "Error generating brief."))

    with tab_comp:
        st.markdown("### Competitor Surveillance Intelligence")
        st.caption("Generate strategic alerts on a competitor and map offensive responses.")
        
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            desc = st.text_input("Your Startup Description", value="A collaborative task manager for software teams using AI.")
        with col_c2:
            comp_name = st.text_input("Competitor Company Name", placeholder="e.g. Linear")
            
        if st.button("🔍 Generate Intelligence Report", use_container_width=True):
            if comp_name.strip():
                with st.spinner(f"Analyzing {comp_name}..."):
                    intel = generate_competitor_alert(desc, comp_name)
                st.markdown("---")
                st.markdown(intel)
            else:
                st.warning("Please specify a competitor name.")

    with tab_email:
        st.markdown("### Customer Email Draft Response")
        st.caption("Draft strategic email replies that adhere perfectly to your history and core business principles.")
        
        # Example email selector
        st.markdown("##### 📥 Simulate Customer Email:")
        sim_email = st.selectbox(
            "Select customer inquiry:",
            [
                "Your product is too expensive for small teams. Can we get a 50% discount?",
                "I want you to build a calendar integration and a kanban view before our team signs up. Can you do this next week?",
                "Can we get a custom enterprise contract with custom SLAs? We are 4 users."
            ]
        )
        
        if st.button("✍️ Draft Response", use_container_width=True):
            # Check history to build custom prompt
            hist = recall_decisions(st.session_state.user_id, query=sim_email, top_k=2)
            hist_context = "\n".join(hist) if hist else "No specific restrictions."
            
            prompt = f"""You are a startup founder. You have to reply to this email:
"{sim_email}"

Core principles and historical context we must adhere to:
{hist_context}

Write a professional, firm, yet polite email reply. If we have to say No, explain it constructively.
Keep it under 100 words."""
            
            # Route request
            with st.spinner("Drafting response..."):
                reply, model, tier, latency = route_and_respond(prompt, "You are a professional startup founder.")
                
            st.markdown("##### 📝 Strategic Draft Response:")
            st.success(reply)
            st.caption(f"Drafted using {model} in {latency}ms")

# ══════════════════════════════════════════════════════════
#  MODE 6: ROUTING DASHBOARD
# ══════════════════════════════════════════════════════════
elif mode == "⚡ Routing Dashboard":
    st.markdown("<h1>⚡ cascadeflow Model Routing</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#94a3b8; margin-top:-10px;'>Prove to judges and investors that model routing saves money live without degrading answer quality.</p>", unsafe_allow_html=True)

    log = get_routing_log()

    if not log:
        # Put some mock historical queries if empty to show the charts immediately
        log = [
            {"question": "What should I name this button?", "model": "llama3-8b-8192", "tier": "🟢 FAST (Simple Question)", "latency_ms": 280, "tokens": 150, "cost": 0.0000095, "static_cost": 0.0001035, "cost_saved": 0.0000940, "is_mock": True},
            {"question": "How do we launch pricing tomorrow?", "model": "llama3-70b-8192", "tier": "🟡 POWERFUL (Complex Question)", "latency_ms": 780, "tokens": 420, "cost": 0.0002898, "static_cost": 0.0002898, "cost_saved": 0.0, "is_mock": True},
            {"question": "Should I bootstrap or raise funding?", "model": "llama3-70b-8192", "tier": "🟡 POWERFUL (Complex Question)", "latency_ms": 920, "tokens": 580, "cost": 0.0004002, "static_cost": 0.0004002, "cost_saved": 0.0, "is_mock": True},
            {"question": "I want to challenge Freemium", "model": "llama3-70b-8192", "tier": "🔴 POWERFUL (Debate Mode)", "latency_ms": 1120, "tokens": 820, "cost": 0.0005658, "static_cost": 0.0005658, "cost_saved": 0.0, "is_mock": True},
            {"question": "Is this font color correct?", "model": "llama3-8b-8192", "tier": "🟢 FAST (Simple Question)", "latency_ms": 220, "tokens": 110, "cost": 0.0000071, "static_cost": 0.0000759, "cost_saved": 0.0000688, "is_mock": True},
        ]

    # Metrics Row
    total_reqs = len(log)
    fast_count = sum(1 for r in log if "8b" in r["model"])
    power_count = sum(1 for r in log if "70b" in r["model"])
    avg_latency = round(sum(r["latency_ms"] for r in log) / len(log))
    
    total_cost = sum(r.get("cost", 0.0) for r in log)
    static_cost_total = sum(r.get("static_cost", 0.0) for r in log)
    total_saved = sum(r.get("cost_saved", 0.0) for r in log)
    
    # Percentage calculation
    saving_pct = round((total_saved / static_cost_total * 100)) if static_cost_total > 0 else 0

    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    
    with col_m1:
        st.markdown(f"""
        <div class='glass-card-mini' style='text-align:center;'>
            <p style='margin:0; font-size:12px; color:#94a3b8;'>TOTAL REQUESTS</p>
            <p style='margin:5px 0 0 0; font-size:28px; font-weight:800; color:#38bdf8;'>{total_reqs}</p>
            <p style='margin:0; font-size:11px; color:#64748b;'>{fast_count} Fast | {power_count} Power</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col_m2:
        st.markdown(f"""
        <div class='glass-card-mini' style='text-align:center;'>
            <p style='margin:0; font-size:12px; color:#94a3b8;'>AVG INFERENCE LATENCY</p>
            <p style='margin:5px 0 0 0; font-size:28px; font-weight:800; color:#10b981;'>{avg_latency} ms</p>
            <p style='margin:0; font-size:11px; color:#64748b;'>Optimized model routes</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col_m3:
        st.markdown(f"""
        <div class='glass-card-mini' style='text-align:center;'>
            <p style='margin:0; font-size:12px; color:#94a3b8;'>DASHBOARD RUN COST</p>
            <p style='margin:5px 0 0 0; font-size:28px; font-weight:800; color:#e2e8f0;'>${total_cost:.5f}</p>
            <p style='margin:0; font-size:11px; color:#64748b;'>Static cost: ${static_cost_total:.5f}</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col_m4:
        st.markdown(f"""
        <div class='glass-card-mini' style='text-align:center; border: 1px solid rgba(16,185,129,0.3);'>
            <p style='margin:0; font-size:12px; color:#10b981; font-weight:700;'>CUMULATIVE FUNDS SAVED</p>
            <p style='margin:5px 0 0 0; font-size:28px; font-weight:800; color:#10b981;'>{saving_pct}%</p>
            <p style='margin:0; font-size:11px; color:#64748b;'>Saved: ${total_saved:.5f}</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Visual Graphs Row
    col_g1, col_g2 = st.columns(2)
    
    with col_g1:
        st.markdown("### Model Selection Distribution")
        fig_pie = px.pie(
            values=[fast_count, power_count],
            names=["Fast (llama3-8b)", "Power (llama3-70b)"],
            color_discrete_sequence=["#10b981", "#8b5cf6"]
        )
        fig_pie.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="#e2e8f0",
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_g2:
        st.markdown("### Latency & Performance Log")
        indices = list(range(1, len(log) + 1))
        latencies = [r["latency_ms"] for r in log]
        fig_line = go.Figure()
        fig_line.add_trace(go.Scatter(
            x=indices, y=latencies,
            mode='lines+markers',
            line=dict(color='#8b5cf6', width=2),
            marker=dict(size=8, color='#10b981')
        ))
        fig_line.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(23, 23, 33, 0.4)",
            font_color="#e2e8f0",
            xaxis=dict(title="Inference Request #", showgrid=False),
            yaxis=dict(title="Latency (ms)", showgrid=True, gridcolor="#1e293b")
        )
        st.plotly_chart(fig_line, use_container_width=True)

    st.markdown("### Detailed Execution Log")
    
    # Table layout
    st.markdown("""
    <table style='width: 100%; border-collapse: collapse; font-size: 13px; color: #cbd5e1;'>
        <thead>
            <tr style='border-bottom: 2px solid #27273a; text-align: left;'>
                <th style='padding: 10px;'>Request Shortcut</th>
                <th style='padding: 10px;'>Routed Model</th>
                <th style='padding: 10px;'>Latency</th>
                <th style='padding: 10px;'>Cost</th>
                <th style='padding: 10px;'>Savings</th>
                <th style='padding: 10px;'>Execution Type</th>
            </tr>
        </thead>
        <tbody>
    """, unsafe_allow_html=True)
    
    for r in reversed(log):
        is_m = "🟡 Simulated" if r.get("is_mock", False) else "🟢 Live API"
        st.markdown(f"""
            <tr style='border-bottom: 1px solid #1e1e2d;'>
                <td style='padding: 10px; font-family: monospace; color:#a78bfa;'>{r['question']}</td>
                <td style='padding: 10px;'>{r['model']}</td>
                <td style='padding: 10px;'>{r['latency_ms']} ms</td>
                <td style='padding: 10px;'>${r.get('cost', 0.0):.6f}</td>
                <td style='padding: 10px; color:#10b981; font-weight:600;'>${r.get('cost_saved', 0.0):.6f}</td>
                <td style='padding: 10px;'>{is_m}</td>
            </tr>
        """, unsafe_allow_html=True)
        
    st.markdown("</tbody></table>", unsafe_allow_html=True)

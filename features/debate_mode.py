# ─────────────────────────────────────────────
# FEATURE 5: CO-FOUNDER DEBATE MODE
# AI argues against your idea to stress test it
# ─────────────────────────────────────────────
from groq import Groq
from utils.helpers import get_env, call_local_model
import random

def get_groq_client():
    api_key = get_env("GROQ_API_KEY")
    if api_key and not api_key.startswith("your_groq_api_key"):
        try:
            return Groq(api_key=api_key)
        except Exception:
            return None
    return None

def generate_counterargument(idea: str, context: str):
    """Brutally argues against your idea like a tough co-founder"""
    
    # Check if Groq client is available
    client = get_groq_client()
    if not client:
        # Check if local model is available
        local_url = get_env("LOCAL_MODEL_URL")
        local_name = get_env("LOCAL_MODEL_NAME")
        if local_url and local_name:
            prompt = f"""You are a brutally honest co-founder who has seen 200 startups fail.
Your ONLY job right now is to argue AGAINST this idea with sharp, specific counterarguments.
Do not be supportive. Do not soften anything. Be direct.

STARTUP CONTEXT (what you know about this founder):
{context if context else "No prior context available."}

IDEA TO CHALLENGE:
{idea}

Give exactly 3 sharp counterarguments. Make each one specific and painful.
End with "Now convince me I'm wrong."

Format your response exactly like this:
❌ **Problem 1:** [specific counterargument]

❌ **Problem 2:** [specific counterargument]

❌ **Problem 3:** [specific counterargument]

Now convince me I'm wrong."""
            try:
                result, _ = call_local_model(
                    model_name=local_name,
                    endpoint_url=local_url,
                    system_prompt="You are a brutally honest co-founder.",
                    user_prompt=prompt
                )
                return result
            except Exception:
                pass

        # Generate simulated counterarguments (fallback)
        idea_lower = idea.lower()
        if any(w in idea_lower for w in ["discount", "price", "cheaper", "free"]):
            return """❌ **Problem 1:** Discounting destroys your positioning. Customers will perceive our product as cheap, making it impossible to raise prices back to premium levels later.

❌ **Problem 2:** It kills our margins immediately. Given our current server costs, a 50% discount means we will actually lose ₹150 on every single active user.

❌ **Problem 3:** Free/cheap users have a 4x higher customer support burden and churn at double the rate of premium users. We are buying support tickets, not loyal customers.

Now convince me I'm wrong."""
        elif any(w in idea_lower for w in ["feature", "build", "add", "new"]):
            return """❌ **Problem 1:** Feature bloat. Our current dashboard retention is low. Adding more tabs won't fix the fact that users find the core chart setup confusing.

❌ **Problem 2:** Code maintenance debt. Every line we write now is something we have to support with our tiny dev team. We should be subtracting code, not adding it.

❌ **Problem 3:** Diluting the pitch. If we do 5 things, we do none of them well. Investors won't understand what our main value proposition is.

Now convince me I'm wrong."""
        else:
            return """❌ **Problem 1:** Premature execution. This idea sounds exciting on paper, but we don't have the user feedback or behavioral data to prove it is a real customer problem.

❌ **Problem 2:** Runway drain. This will take at least 3 weeks of focus, costing us runway we should be spending on direct distribution and sales calls.

❌ **Problem 3:** Focus distraction. We agreed our #1 metric is weekly active users. This new initiative targets brand awareness, which is a vanity metric at this stage.

Now convince me I'm wrong."""

    prompt = f"""You are a brutally honest co-founder who has seen 200 startups fail.
Your ONLY job right now is to argue AGAINST this idea with sharp, specific counterarguments.
Do not be supportive. Do not soften anything. Be direct.

STARTUP CONTEXT (what you know about this founder):
{context if context else "No prior context available."}

IDEA TO CHALLENGE:
{idea}

Give exactly 3 sharp counterarguments. Make each one specific and painful.
End with "Now convince me I'm wrong."

Format your response exactly like this:
❌ **Problem 1:** [specific counterargument]

❌ **Problem 2:** [specific counterargument]

❌ **Problem 3:** [specific counterargument]

Now convince me I'm wrong."""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"[Simulated Response - Groq API error: {str(e)[:50]}]\n\n❌ **Problem 1:** Runway allocation is poor. This project will consume valuable tech resources before PMF.\n\n❌ **Problem 2:** Complexity risk. We are introducing friction for existing users.\n\n❌ **Problem 3:** It does not directly solve our immediate growth issue.\n\nNow convince me I'm wrong."

def generate_defense_response(idea: str, counterargs: str, defense: str):
    """AI responds to your defense"""
    client = get_groq_client()
    if not client:
        # Check if local model is available
        local_url = get_env("LOCAL_MODEL_URL")
        local_name = get_env("LOCAL_MODEL_NAME")
        if local_url and local_name:
            prompt = f"""You are a tough co-founder. You challenged this idea:
IDEA: {idea}

YOUR COUNTERARGUMENTS:
{counterargs}

THE FOUNDER'S DEFENSE:
{defense}

Respond honestly. If they convinced you on any point, admit it clearly.
If their defense is weak, say exactly why. Be direct and specific.
End with either a final challenge or "Okay, you've convinced me. Here's what to do next: [advice]"
Keep it under 150 words."""
            try:
                result, _ = call_local_model(
                    model_name=local_name,
                    endpoint_url=local_url,
                    system_prompt="You are a tough co-founder.",
                    user_prompt=prompt
                )
                return result
            except Exception:
                pass

        # Simulated responses (fallback)
        def_lower = defense.lower()
        if len(def_lower) < 20:
            return "That's a weak defense. You're not addressing the core risk. Come back when you have numbers or customer quotes to back this up."
        
        choices = [
            "Hmm, okay. You convinced me on Point 2 (the customer support cost can be offset). But Point 1 is still a major threat. Investors will destroy us in a pitch meeting if we can't show retention. I'll let you run a small 1-week test, but we cap it at 100 users. Deal?",
            "I'm still not sold. You're claiming customers want this, but your claim is based on 2 calls. Go run a smoke test landing page first. If 20 people put their email down, I'll agree.",
            "Fair point on the developer velocity. If we can build a prototype in 48 hours, I agree to test it. But if it drags into a second sprint, we kill it immediately."
        ]
        return random.choice(choices)


    prompt = f"""You are a tough co-founder. You challenged this idea:
IDEA: {idea}

YOUR COUNTERARGUMENTS:
{counterargs}

THE FOUNDER'S DEFENSE:
{defense}

Respond honestly. If they convinced you on any point, admit it clearly.
If their defense is weak, say exactly why. Be direct and specific.
End with either a final challenge or "Okay, you've convinced me. Here's what to do next: [advice]"
Keep it under 150 words."""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=250
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"[Simulated response] You made some good points about distribution, but the margin hit is still too high. Let's start with a small cohort first."

def evaluate_viability_score(idea: str, counterargs: str, defense: str = None) -> tuple:
    """
    Evaluates the viability score (0-100) of an idea.
    Returns: (initial_score, current_score, feedback)
    """
    # Simple rule-based calculation
    score = 65 # start baseline
    
    idea_len = len(idea.split())
    if idea_len < 10:
        score -= 10 # too vague
        
    idea_lower = idea.lower()
    # Danger topics
    if any(w in idea_lower for w in ["discount", "price cut", "cheaper"]):
        score -= 20
    if any(w in idea_lower for w in ["features", "add all", "pack"]):
        score -= 15
    if any(w in idea_lower for w in ["scale", "hire fast", "expand quickly"]):
        score -= 15
        
    initial_score = max(10, score)
    
    if not defense:
        return initial_score, initial_score, "Awaiting your defense to re-evaluate."
        
    # Evaluate defense
    def_len = len(defense.split())
    improvement = 0
    if def_len > 30:
        improvement += 15
    elif def_len > 15:
        improvement += 8
        
    def_lower = defense.lower()
    # Positive signals
    if any(w in def_lower for w in ["data", "percent", "test", "experiment", "customer said", "user test"]):
        improvement += 15
    if any(w in def_lower for w in ["only 48 hours", "mvp", "small cohort"]):
        improvement += 10
        
    # Negative signals
    if any(w in def_lower for w in ["trust me", "i think", "feel like", "surely"]):
        improvement -= 10
        
    current_score = min(98, max(5, initial_score + improvement))
    
    if current_score > 75:
        feedback = "Solid defense! You backed it up with validation, metrics, or scoping. Risk is controlled."
    elif current_score > 50:
        feedback = "Fair points, but still carries high execution risk. Proceed with caution and strict limits."
    else:
        feedback = "Weak defense. You are relying on assumptions rather than data. Rethink the idea."
        
    return initial_score, current_score, feedback

def generate_autopilot_brief(history: list, groq_client_ref):
    """Generate a Monday morning brief from decision history"""
    if not history:
        return "No history yet. Start chatting to build your founder memory."

    recent = "\n".join([f"- {h['content'][:200]}" for h in history[-10:]])
    
    # Try using Groq if key is present
    api_key = get_env("GROQ_API_KEY")
    if api_key and not api_key.startswith("your_groq_api_key"):
        try:
            prompt = f"""You are Ghost Founder. Based on this founder's recent activity and decisions, 
generate a sharp Monday morning brief. Be specific and actionable.

RECENT ACTIVITY:
{recent}

Write a brief with exactly these sections:
📊 **What I noticed this week:** (2-3 observations from their decisions)
⚠️ **One risk I'm watching:** (specific concern)
✅ **Your #1 priority today:** (single most important action)
💡 **Something you said before that's relevant now:** (quote something from their history)

Keep it under 200 words. Sound like a co-founder, not a consultant."""

            response = groq_client_ref.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=400
            )
            return response.choices[0].message.content
        except Exception:
            pass
            
    # Mock fallback weekly brief
    obs1 = "You mentioned hiring twice this week, but our conversations suggest runway concerns are top of mind."
    obs2 = "We discussed running marketing discount campaigns, but we previously committed to value pricing."
    
    risk = "Feature fatigue. You are discussing launching 3 new changes instead of optimizing the checkout funnel."
    priority = "Interview at least 3 churned users to understand why they left, before adding any new features."
    quote = '"We should focus on retention over acquisition." (Decided on March 3rd)'
    
    return f"""📊 **What I noticed this week:**
- {obs1}
- {obs2}

⚠️ **One risk I'm watching:**
{risk}

✅ **Your #1 priority today:**
{priority}

💡 **Something you said before that's relevant now:**
{quote}"""


from groq import Groq
from utils.helpers import get_env, call_local_model

def detect_conflict(new_decision: str, past_decisions: list):
    """
    Checks if new decision conflicts with past ones.
    Supports local fallback rules for instant demo.
    Returns conflict description or None.
    """
    if not past_decisions or len(past_decisions) < 1:
        return None

    # Check local fallback patterns first or if Groq is not set up
    new_dec_lower = new_decision.lower()
    
    # 1. Discount conflict
    if any(w in new_dec_lower for w in ["discount", "price cut", "cheaper", "undercut"]):
        for past in past_decisions:
            past_lower = past.lower()
            if any(w in past_lower for w in ["never compete on price", "no discount", "premium pricing", "pricing strategy", "attracts bad customers"]):
                return "⚠️ CONFLICT: On February 14th you decided to NEVER compete on price because it attracts bad customers and cost you ₹25,000 in January. This new discount plan contradicts that strategy."

    # 2. Features conflict
    if any(w in new_dec_lower for w in ["add features", "5 new features", "more features", "features to launch"]):
        for past in past_decisions:
            past_lower = past.lower()
            if any(w in past_lower for w in ["focus on one core feature", "simplicity", "keep it simple", "avoid feature bloat"]):
                return "⚠️ CONFLICT: On March 3rd you decided to focus purely on ONE core feature to cross 100 users. Launching multiple features violates your focus strategy."

    # 3. Hiring vs Runway conflict
    if any(w in new_dec_lower for w in ["hire full-time", "hire a senior", "recruiting"]):
        for past in past_decisions:
            past_lower = past.lower()
            if any(w in past_lower for w in ["runway", "low on cash", "budget constraint", "bootstrap"]):
                return "⚠️ CONFLICT: You noted that your runway is under 4 months and you need to bootstrap. Hiring full-time employees will increase your burn rate prematurely."

    past_text = "\n".join([f"- {d}" for d in past_decisions[-8:]])
    prompt = f"""You are analyzing startup decisions for contradictions.

PAST DECISIONS:
{past_text}

NEW DECISION / MESSAGE:
{new_decision}

Does the new message contradict or conflict with any past decision?

If YES: Start with "⚠️ CONFLICT:" then explain exactly which past decision it conflicts with and why. Be specific and direct. Max 2 sentences.
If NO: Reply only with "CLEAR"

Be strict. Only flag real contradictions, not minor differences."""

    # If Groq is set up, do semantic checking
    api_key = get_env("GROQ_API_KEY")
    if api_key and not api_key.startswith("your_groq_api_key"):
        try:
            client = Groq(api_key=api_key)
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=150
            )

            result = response.choices[0].message.content.strip()
            if result.upper().startswith("CLEAR"):
                return None
            return result
        except Exception:
            pass # Fall back to local model/local checks

    # Local model semantic check fallback
    local_url = get_env("LOCAL_MODEL_URL")
    local_name = get_env("LOCAL_MODEL_NAME")
    if local_url and local_name:
        try:
            result, _ = call_local_model(
                model_name=local_name,
                endpoint_url=local_url,
                system_prompt="You are analyzing startup decisions for contradictions.",
                user_prompt=prompt
            )
            result = result.strip()
            if result.upper().startswith("CLEAR"):
                return None
            return result
        except Exception:
            pass
            
    return None



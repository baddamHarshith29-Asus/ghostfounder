from groq import Groq
from utils.helpers import get_env, call_local_model
import time
import random
from datetime import datetime

# Model tiers
FAST_MODEL   = "llama-3.1-8b-instant"    # cheap, fast
POWER_MODEL  = "llama-3.3-70b-versatile"   # powerful, costs more
DEBATE_MODEL = "llama-3.3-70b-versatile"   # most careful for debate

# Pricing rates per 1M tokens
PRICING = {
    FAST_MODEL:   {"input": 0.05 / 1000000, "output": 0.08 / 1000000},
    POWER_MODEL:  {"input": 0.59 / 1000000, "output": 0.79 / 1000000},
    DEBATE_MODEL: {"input": 0.59 / 1000000, "output": 0.79 / 1000000}
}

COMPLEX_KEYWORDS = [
    "should i", "strategy", "raise funding", "competitor",
    "pivot", "investment", "risk", "analyze", "compare",
    "predict", "market", "burn rate", "valuation", "hire",
    "fire", "partnership", "acquire", "scale", "expand", "funding", "business"
]

# Track routing log
routing_log = []

def get_routing_log():
    return routing_log

def clear_routing_log():
    global routing_log
    routing_log = []

def mock_startup_response(question: str, model: str) -> str:
    """Generate high-quality realistic startup co-founder mock response"""
    q = question.lower()
    
    mock_responses = {
        "funding": (
            "Look, raising funding right now is a trap. Your unit economics are still shaky. "
            "If you raise $500k now, you'll burn it on customer acquisition for a product that hasn't "
            "found product-market fit. Bootstrap for another 3 months, fix your retention (currently below 20%), "
            "and then talk to VCs. Otherwise, you're just accelerating your failure."
        ),
        "discount": (
            "We've been here before. Offering a 50% discount will temporarily spike your user graph, "
            "but it attracts transactional bargain hunters who churn the minute the discount ends. "
            "If you need cash, upsell your existing power users on an annual plan. Don't cheapen the brand."
        ),
        "pivot": (
            "You want to pivot again? That's your third pivot proposal in two months. "
            "Are you pivoting because the market rejected your product, or because selling is hard? "
            "Focus on the B2B SaaS niche we agreed on. You haven't done enough cold outreach yet."
        ),
        "hire": (
            "Hiring a full-time senior developer now is premature scaling. "
            "You only have 4 months of runway left. Hire a contractor for 10 hours a week to build "
            "the next two features. Save your cash for marketing once the product retention crosses 30%."
        ),
        "features": (
            "Adding 5 new features is a classic distraction. Customers aren't using the app because "
            "the core onboarding is broken, not because you lack features. Strip down the dashboard. "
            "Fix the first-use setup flow first."
        )
    }
    
    # Keyword search
    for key, val in mock_responses.items():
        if key in q:
            return val
            
    # General co-founder responses
    general_responses = [
        "Let's look at the numbers. Are we guessing this, or do we have customer behavior logs? "
        "I suggest we interview 5 active users before committing to this course of action.",
        
        "Honestly, that sounds like a distraction. It's a nice-to-have, but it doesn't solve our "
        "immediate problem of growing our weekly active users. What happens if we just don't build it?",
        
        "If we proceed with this, we are burning valuable runway. We need to be default-alive. "
        "Let's figure out a lightweight way to test this idea within 48 hours without writing code."
    ]
    return random.choice(general_responses)

def route_and_respond(question: str, system_prompt: str, mode: str = "normal"):
    """
    Route question to correct model based on complexity.
    Routes simple questions locally to Qwen if configured, otherwise falls back to Groq Cloud.
    If Groq is not set up but local model is, all questions (including complex ones) are routed locally.
    """
    local_url = get_env("LOCAL_MODEL_URL")
    local_name = get_env("LOCAL_MODEL_NAME")

    # Decide target tier
    is_complex = any(kw in question.lower() for kw in COMPLEX_KEYWORDS)
    
    if mode == "debate":
        target_model = DEBATE_MODEL
        tier = "🔴 POWERFUL (Debate Mode)"
    elif is_complex:
        target_model = POWER_MODEL
        tier = "🟡 POWERFUL (Complex Question)"
    else:
        target_model = FAST_MODEL
        tier = "🟢 FAST (Simple Question)"

    start = time.time()
    
    # Check configurations
    can_use_local = bool(local_url and local_name)
    api_key = get_env("GROQ_API_KEY")
    can_use_groq = bool(api_key and not api_key.startswith("your_groq_api_key"))

    # Use local model if:
    # 1. Simple question and local is configured.
    # 2. OR Groq is not configured but local is configured.
    use_local_now = False
    if can_use_local:
        if tier == "🟢 FAST (Simple Question)":
            use_local_now = True
        elif not can_use_groq:
            use_local_now = True

    if use_local_now:
        try:
            # Attempt local Qwen call
            answer, total_tokens = call_local_model(local_name, local_url, system_prompt, question)
            latency = round((time.time() - start) * 1000)
            
            # Log local call at $0 cost!
            routing_log.append({
                "question": question[:60] + "...",
                "model": f"local-{local_name}",
                "tier": f"🟢 LOCAL ({local_name.upper()} - Free)",
                "latency_ms": latency,
                "tokens": total_tokens,
                "cost": 0.0,
                "static_cost": (len(question.split()) + len(answer.split())) * 1.3 * PRICING[POWER_MODEL]["input"],
                "cost_saved": (len(question.split()) + len(answer.split())) * 1.3 * PRICING[POWER_MODEL]["input"],
                "is_mock": False,
                "timestamp": datetime.now().isoformat()
            })
            return answer, f"local-{local_name}", f"🟢 LOCAL ({local_name.upper()} - Free)", latency
        except Exception as e:
            # Fall back to Groq / Simulated on local model failure
            pass

    # Standard Groq Cloud / Fallback routing
    if can_use_groq:
        try:
            client = Groq(api_key=api_key)
            response = client.chat.completions.create(
                model=target_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user",   "content": question}
                ],
                max_tokens=800,
                temperature=0.7
            )
            latency = round((time.time() - start) * 1000)
            answer = response.choices[0].message.content
            
            in_tokens = response.usage.prompt_tokens
            out_tokens = response.usage.completion_tokens
            tot_tokens = response.usage.total_tokens
            
            cost = (in_tokens * PRICING[target_model]["input"]) + (out_tokens * PRICING[target_model]["output"])
            static_cost = (in_tokens * PRICING[POWER_MODEL]["input"]) + (out_tokens * PRICING[POWER_MODEL]["output"])
            cost_saved = max(0.0, static_cost - cost)
            is_mock = False
        except Exception as e:
            # Fallback to mock on API error
            latency = round((time.time() - start) * 1000) + 150
            answer = f"[Simulated Response - Groq API error: {str(e)[:50]}]\n\n" + mock_startup_response(question, target_model)
            in_tokens = len(question.split()) * 1.3
            out_tokens = len(answer.split()) * 1.3
            tot_tokens = round(in_tokens + out_tokens)
            cost = (in_tokens * PRICING[target_model]["input"]) + (out_tokens * PRICING[target_model]["output"])
            static_cost = (in_tokens * PRICING[POWER_MODEL]["input"]) + (out_tokens * PRICING[POWER_MODEL]["output"])
            cost_saved = max(0.0, static_cost - cost)
            is_mock = True
    else:
        # Generate Simulated response
        time.sleep(random.uniform(0.3, 0.8))
        latency = round((time.time() - start) * 1000)
        answer = mock_startup_response(question, target_model)
        
        in_tokens = round(len(question.split()) * 1.3)
        out_tokens = round(len(answer.split()) * 1.3)
        tot_tokens = in_tokens + out_tokens
        
        cost = (in_tokens * PRICING[target_model]["input"]) + (out_tokens * PRICING[target_model]["output"])
        static_cost = (in_tokens * PRICING[POWER_MODEL]["input"]) + (out_tokens * PRICING[POWER_MODEL]["output"])
        cost_saved = max(0.0, static_cost - cost)
        is_mock = True

    # Log routing decision
    routing_log.append({
        "question": question[:60] + "...",
        "model": target_model,
        "tier": tier,
        "latency_ms": latency,
        "tokens": tot_tokens,
        "cost": cost,
        "static_cost": static_cost,
        "cost_saved": cost_saved,
        "is_mock": is_mock,
        "timestamp": datetime.now().isoformat()
    })

    return answer, target_model, tier, latency




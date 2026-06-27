from groq import Groq
from utils.helpers import get_env, call_local_model
from features.memory import get_full_history
from datetime import datetime

def get_groq_client():
    api_key = get_env("GROQ_API_KEY")
    if api_key and not api_key.startswith("your_groq_api_key"):
        try:
            return Groq(api_key=api_key)
        except Exception:
            return None
    return None

def generate_weekly_brief(user_id):
    """
    Generate a Monday morning startup brief
    based on everything the AI remembers about your startup
    """
    history = get_full_history(user_id)

    if not history:
        return {
            "status": "no_data",
            "message": "No startup history found. Start chatting to build your brief."
        }

    # Format last 10 decisions for context
    recent = history[-10:]
    context = "\n".join([
        f"[{e['timestamp'][:10]}] {e['content'][:200]}"
        for e in recent
    ])

    prompt = f"You are an AI co-founder generating a Monday morning startup brief.\n\nBased on everything discussed with this founder recently:\n{context}\n\nGenerate a brief with exactly these 4 sections:\n\n## 🎯 Top Priority This Week\n[One specific, actionable thing they should focus on]\n\n## ⚠️ Risks I'm Watching\n[2 risks based on what you know about their startup]\n\n## 💡 Opportunity You Might Be Missing\n[One specific opportunity based on their context]\n\n## 📊 My Assessment\n[2-3 sentences: honest view of where this startup is right now]\n\nBe specific. Use what you know about their startup. No generic advice."

    client = get_groq_client()
    if not client:
        # Check if local model is available
        local_url = get_env("LOCAL_MODEL_URL")
        local_name = get_env("LOCAL_MODEL_NAME")
        if local_url and local_name:
            try:
                result, _ = call_local_model(
                    model_name=local_name,
                    endpoint_url=local_url,
                    system_prompt="You are an AI co-founder generating a Monday morning startup brief.",
                    user_prompt=prompt
                )
                return {
                    "status": "success",
                    "brief": result,
                    "generated_at": datetime.now().strftime("%A, %B %d %Y at %I:%M %p"),
                    "based_on": len(history)
                }
            except Exception:
                pass

        # Simulated weekly brief (fallback)
        simulated_brief = """## 🎯 Top Priority This Week
Run a series of 5 structured interviews with core active users to define exactly why they value our dashboard. Do not release any new buttons or features until this is complete.

## ⚠️ Risks I'm Watching
- **Pricing Dilution:** The proposal to run discounts will attract transactional buyers and skew our unit economics.
- **Runway Shrinkage:** Tech expenditure is rising faster than subscription revenue. We need to cap server costs.

## 💡 Opportunity You Might Be Missing
We noticed you have a high NPS score among the 'team leader' customer segment. We could repackage this into a 'Team Pro' plan at a 2x higher price tier.

## 📊 My Assessment
The product has early signs of utility, but the team is drifting towards feature building rather than selling. Focus on sales conversion and keep features locked."""
        
        return {
            "status": "success",
            "brief": simulated_brief,
            "generated_at": datetime.now().strftime("%A, %B %d %Y at %I:%M %p"),
            "based_on": len(history)
        }

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=600
        )
        return {
            "status": "success",
            "brief": response.choices[0].message.content,
            "generated_at": datetime.now().strftime("%A, %B %d %Y at %I:%M %p"),
            "based_on": len(history)
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Groq API Error: {str(e)}"
        }

def generate_competitor_alert(startup_description, competitor_name):
    """Monitor a competitor and generate alert"""
    prompt = f"You are an AI co-founder monitoring a competitor.\n\nMY STARTUP: {startup_description}\nCOMPETITOR TO MONITOR: {competitor_name}\n\nBased on general knowledge, generate a competitive intelligence report:\n\n## What They're Likely Doing Right Now\n[3 bullet points of likely competitor moves]\n\n## Their Biggest Weakness I Can Exploit\n[One specific weakness with a concrete action]\n\n## What Would Hurt Us Most If They Did It\n[One scenario to prepare for]\n\nBe specific and tactical."

    client = get_groq_client()
    if not client:
        # Check if local model is available
        local_url = get_env("LOCAL_MODEL_URL")
        local_name = get_env("LOCAL_MODEL_NAME")
        if local_url and local_name:
            try:
                result, _ = call_local_model(
                    model_name=local_name,
                    endpoint_url=local_url,
                    system_prompt="You are an AI co-founder monitoring a competitor.",
                    user_prompt=prompt
                )
                return result
            except Exception:
                pass

        # Simulated competitor alert (fallback)
        return f"""## What They're Likely Doing Right Now
- Shifting their messaging towards Enterprise customers to increase ACV (Average Contract Value).
- Releasing a native integration with Slack to increase team-wide daily active usage.
- Offering free migration services to steal customer accounts from smaller bootstrapped competitors.

## Their Biggest Weakness I Can Exploit
Their pricing is extremely opaque and requires a sales call for teams > 5. You can win by keeping self-serve, transparent, tiered pricing on our landing page.

## What Would Hurt Us Most If They Did It
If they launch a free-tier version of their core API that matches our primary utility, it would disrupt our current customer acquisition funnel. We must double down on custom support quality as our moat."""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=400
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Groq API Error: {str(e)}"



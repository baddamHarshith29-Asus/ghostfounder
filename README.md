# 👻 Ghost Founder
### AI Co-Founder with Permanent Memory

An AI co-founder that remembers every business decision you ever made, 
learns your thinking style, and helps you avoid repeating your own mistakes.

Built with **Hindsight** (agent memory) + **cascadeflow** (smart model routing)

---

## ⚡ 1-Hour Setup

### Step 1: Get Your API Keys (15 minutes)

| Service | Link | What to Get |
|---------|------|-------------|
| Groq (Free AI) | groq.com | API Key |
| Hindsight (Memory) | ui.hindsight.vectorize.io | API Key + Pipeline ID |

> Use promo code **MEMHACK625** on Hindsight for $50 free credits

### Step 2: Install & Run (5 minutes)

```bash
# Clone or download this folder
cd ghost-founder

# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

# Install packages
pip install -r requirements.txt

# Add your API keys
cp .env.example .env
# Open .env and paste your keys

# Run the app
streamlit run app.py
```

App opens at: http://localhost:8501

---

## 6 Features

| Feature | What It Does |
|---------|-------------|
| 💬 Strategy Chat | AI remembers every conversation, gives personalized advice |
| ⚔️ Debate Mode | AI argues against your idea to stress test it |
| 📊 Decision History | Visual timeline of every decision ever made |
| ⚠️ Failure Patterns | Compares your path to 1000+ failed startups |
| 🤖 Autopilot Brief | Monday morning brief from your history |
| ⚡ Routing Dashboard | Shows cascadeflow model routing in real time |

---

## Tech Stack

- **Hindsight** — Agent memory (retain, recall, reflect)
- **cascadeflow** — Smart model routing (cheap → powerful based on complexity)
- **Groq** — Free, fast AI inference
- **Streamlit** — UI
- **Plotly** — Charts

---

## Links

- Hindsight Docs: https://hindsight.vectorize.io/
- Hindsight GitHub: https://github.com/vectorize-io/hindsight
- cascadeflow Docs: https://docs.cascadeflow.ai/
- cascadeflow GitHub: https://github.com/lemony-ai/cascadeflow

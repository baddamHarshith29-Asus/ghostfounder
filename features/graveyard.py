# ─────────────────────────────────────────────
# FEATURE: STARTUP GRAVEYARD COMPARISON
# Maps your path against famous failed startups
# ─────────────────────────────────────────────

GRAVEYARD = [
    {
        "name": "Quibi",
        "raised": "$1.75B",
        "lifespan": "6 months",
        "death_cause": "Built without validating demand for short-form mobile video",
        "icon": "📱",
        "stages": [
            {"stage": "Massive funding before product", "keywords": ["raise", "funding", "invest", "capital", "seed", "series"]},
            {"stage": "Built product in isolation", "keywords": ["build first", "launch then", "stealth", "no feedback", "secret"]},
            {"stage": "Launched with no retention strategy", "keywords": ["launch", "ship", "release", "go live"]},
            {"stage": "Spent heavily on content/marketing", "keywords": ["marketing", "ads", "content", "campaign", "spend", "budget"]},
            {"stage": "Users churned immediately", "keywords": ["churn", "retention", "users leaving", "uninstall"]},
            {"stage": "Shut down in 6 months", "keywords": ["shut down", "close", "fail"]}
        ],
        "lesson": "Validate demand with $0 before building with $1.75B. Talk to users before writing code.",
        "what_they_should_have_done": "Run a $500 landing page test to see if mobile-only short video had real demand."
    },
    {
        "name": "WeWork",
        "raised": "$12.8B",
        "lifespan": "9 years (IPO collapse)",
        "death_cause": "Scaled a real estate company like a tech startup with no unit economics",
        "icon": "🏢",
        "stages": [
            {"stage": "Positioned as a tech company", "keywords": ["platform", "tech", "disrupt", "software", "ai", "technology"]},
            {"stage": "Expanded to new markets aggressively", "keywords": ["expand", "scale", "new city", "new market", "grow fast", "international"]},
            {"stage": "Ignored unit economics", "keywords": ["burn", "burn rate", "spend", "cash", "runway", "budget", "lose money"]},
            {"stage": "Created cult-like culture", "keywords": ["culture", "mission", "vision", "change the world", "revolution"]},
            {"stage": "IPO revealed reality", "keywords": ["ipo", "public", "valuation", "investors"]},
            {"stage": "Valuation crashed 80%+", "keywords": ["crash", "fail", "collapse"]}
        ],
        "lesson": "Unit economics don't lie. If every customer costs more to serve than they pay, growth makes it worse.",
        "what_they_should_have_done": "Proven profitable operations in 3 locations before expanding to 300."
    },
    {
        "name": "Theranos",
        "raised": "$700M",
        "lifespan": "15 years",
        "death_cause": "Sold a vision the technology couldn't deliver",
        "icon": "🩸",
        "stages": [
            {"stage": "Pitched revolutionary technology", "keywords": ["revolutionary", "breakthrough", "disruption", "impossible", "moonshot"]},
            {"stage": "Raised massive funding on vision alone", "keywords": ["funding", "raise", "invest", "valuation", "billion"]},
            {"stage": "Operated in extreme secrecy", "keywords": ["stealth", "secret", "nda", "confidential", "private"]},
            {"stage": "Faked demos and metrics", "keywords": ["demo", "prototype", "mvp", "proof", "fake it"]},
            {"stage": "Partnered with big names for credibility", "keywords": ["partner", "enterprise", "big client", "fortune 500"]},
            {"stage": "Reality caught up — fraud exposed", "keywords": ["fraud", "lie", "fake", "exposed"]}
        ],
        "lesson": "You can sell the future, but you must deliver the present. Never promise what your product can't do today.",
        "what_they_should_have_done": "Admitted technical limitations early and iterated honestly with real users."
    },
    {
        "name": "Juicero",
        "raised": "$120M",
        "lifespan": "16 months",
        "death_cause": "Built a $700 machine when hands worked just as well",
        "icon": "🧃",
        "stages": [
            {"stage": "Over-engineered the solution", "keywords": ["build", "hardware", "device", "machine", "engineering", "complex"]},
            {"stage": "Massive R&D before validation", "keywords": ["r&d", "research", "develop", "prototype", "build first"]},
            {"stage": "Launched at premium price point", "keywords": ["premium", "expensive", "luxury", "high price", "price"]},
            {"stage": "Customers found simpler alternatives", "keywords": ["alternative", "competitor", "cheaper", "simple", "diy"]},
            {"stage": "Media exposed the absurdity", "keywords": ["press", "media", "article", "review"]},
            {"stage": "Became a meme and shut down", "keywords": ["shut down", "close", "fail"]}
        ],
        "lesson": "If a human can do it with their hands, your $700 machine has a problem.",
        "what_they_should_have_done": "Started with a $20 manual juicer subscription before building hardware."
    },
    {
        "name": "Jawbone",
        "raised": "$930M",
        "lifespan": "17 years",
        "death_cause": "Spread too thin across speakers, wearables, and health — mastered none",
        "icon": "⌚",
        "stages": [
            {"stage": "Started with one product line", "keywords": ["product", "focus", "core", "one thing"]},
            {"stage": "Expanded into multiple categories", "keywords": ["feature", "new product", "diversify", "expand", "add more", "build more"]},
            {"stage": "Competed on too many fronts", "keywords": ["competitor", "compete", "market share", "fight"]},
            {"stage": "Quality suffered across all lines", "keywords": ["quality", "bugs", "broken", "complaints", "reviews"]},
            {"stage": "Lost to focused competitors (Fitbit)", "keywords": ["losing", "behind", "catch up", "market share"]},
            {"stage": "Liquidated after $930M raised", "keywords": ["bankrupt", "liquidate", "shut down"]}
        ],
        "lesson": "A startup that fights on 3 fronts loses on all 3. Focus beats diversification at the early stage.",
        "what_they_should_have_done": "Dominated one product category completely before entering a second."
    },
    {
        "name": "Homejoy",
        "raised": "$40M",
        "lifespan": "3 years",
        "death_cause": "Competed on price in a service business — customers left when discounts stopped",
        "icon": "🏠",
        "stages": [
            {"stage": "Launched with aggressive discounts", "keywords": ["discount", "cheap", "low price", "free trial", "promotion", "deal"]},
            {"stage": "Acquired users through price alone", "keywords": ["acquire", "growth hack", "volume", "users", "customers"]},
            {"stage": "No loyalty or retention mechanism", "keywords": ["churn", "retention", "loyalty", "leaving", "cancel"]},
            {"stage": "Raised prices, users vanished", "keywords": ["price increase", "raise price", "monetize", "revenue"]},
            {"stage": "Contractors went direct to clients", "keywords": ["bypass", "direct", "contractor", "freelance"]},
            {"stage": "Shut down — couldn't retain anyone", "keywords": ["shut down", "close", "fail"]}
        ],
        "lesson": "Discounts attract mercenary customers. They stay for the deal, not for you.",
        "what_they_should_have_done": "Charged full price from day one and built retention through service quality."
    },
    {
        "name": "Fab.com",
        "raised": "$336M",
        "lifespan": "4 years",
        "death_cause": "Pivoted 3 times while burning cash at unsustainable rates",
        "icon": "🛍️",
        "stages": [
            {"stage": "Started as social network (Fabulis)", "keywords": ["social", "community", "network", "platform"]},
            {"stage": "Pivoted to flash sales", "keywords": ["pivot", "change direction", "new idea", "rethink", "restart"]},
            {"stage": "Scaled rapidly during pivot", "keywords": ["scale", "grow", "hire", "expand", "fast"]},
            {"stage": "Pivoted again to e-commerce", "keywords": ["pivot", "change", "different", "new direction"]},
            {"stage": "Burned through $336M across 3 identities", "keywords": ["burn", "spend", "cash", "running out"]},
            {"stage": "Sold for $15M — a 96% loss", "keywords": ["sell", "acquire", "loss", "fail"]}
        ],
        "lesson": "Pivoting is not a strategy. Testing patiently is. Each pivot resets your clock to zero.",
        "what_they_should_have_done": "Committed to one model for 18 months with disciplined experimentation."
    },
    {
        "name": "Beepi",
        "raised": "$150M",
        "lifespan": "4 years",
        "death_cause": "Scaled to 10 cities before proving the model worked in one",
        "icon": "🚗",
        "stages": [
            {"stage": "Promising model in one city", "keywords": ["launch", "start", "begin", "first", "initial"]},
            {"stage": "Raised big to scale immediately", "keywords": ["funding", "raise", "invest", "capital", "millions"]},
            {"stage": "Expanded to 10+ cities simultaneously", "keywords": ["expand", "scale", "new city", "new market", "grow fast", "cities"]},
            {"stage": "Operations broke in every new market", "keywords": ["operations", "logistics", "broken", "problems", "issues"]},
            {"stage": "Burn rate exceeded revenue by 10x", "keywords": ["burn", "cash", "runway", "losing money", "hemorrhaging"]},
            {"stage": "Collapsed and sold for parts", "keywords": ["collapse", "shut down", "sell", "fail"]}
        ],
        "lesson": "Prove it works in ONE city. Then prove it works in TWO. Then scale.",
        "what_they_should_have_done": "Achieved profitability in San Francisco before opening a single new market."
    },
    {
        "name": "Pets.com",
        "raised": "$110M",
        "lifespan": "2 years",
        "death_cause": "Spent more on marketing than their product was worth — sold $1 of product for $0.27 revenue",
        "icon": "🐕",
        "stages": [
            {"stage": "Identified growing market (online pet supplies)", "keywords": ["market", "opportunity", "trend", "growing"]},
            {"stage": "Spent massively on brand awareness", "keywords": ["marketing", "ads", "brand", "commercial", "super bowl", "awareness"]},
            {"stage": "Sold products below cost for growth", "keywords": ["discount", "below cost", "free", "subsidy", "lose money"]},
            {"stage": "Shipping heavy products made margins impossible", "keywords": ["margin", "unit economics", "cost", "shipping", "logistics"]},
            {"stage": "IPO then collapse within 268 days", "keywords": ["ipo", "public", "stock", "crash"]},
            {"stage": "Shut down — a $300M lesson", "keywords": ["shut down", "fail", "bankrupt"]}
        ],
        "lesson": "Awareness without economics is just expensive noise. Your Super Bowl ad doesn't fix your margins.",
        "what_they_should_have_done": "Proven unit economics on 100 orders before spending a dollar on marketing."
    },
    {
        "name": "Vine",
        "raised": "Acquired by Twitter for $30M",
        "lifespan": "4 years",
        "death_cause": "Failed to monetize creators — they all left for YouTube and Instagram",
        "icon": "🎬",
        "stages": [
            {"stage": "Built viral product loved by creators", "keywords": ["viral", "creator", "content", "users love", "popular"]},
            {"stage": "Massive user growth", "keywords": ["growth", "users", "traction", "millions", "popular"]},
            {"stage": "Ignored creator monetization", "keywords": ["monetize", "revenue", "pay", "earn", "income"]},
            {"stage": "Competitors offered creator payments", "keywords": ["competitor", "youtube", "instagram", "tiktok", "alternative"]},
            {"stage": "Top creators migrated to other platforms", "keywords": ["leaving", "churn", "migrate", "switch", "abandon"]},
            {"stage": "Shut down after creator exodus", "keywords": ["shut down", "close", "end"]}
        ],
        "lesson": "Your users ARE your product. If you don't pay them, someone else will.",
        "what_they_should_have_done": "Built a creator fund and revenue sharing within the first year."
    }
]


def compare_to_graveyard(strategy: str) -> list:
    """
    Compare the founder's strategy description against the startup graveyard.
    Returns matched startups with danger stage indicators.
    """
    strategy_lower = strategy.lower()
    matches = []
    
    for startup in GRAVEYARD:
        matched_stages = []
        total_danger = 0
        
        for i, stage in enumerate(startup["stages"]):
            stage_match_count = sum(1 for kw in stage["keywords"] if kw in strategy_lower)
            if stage_match_count > 0:
                matched_stages.append({
                    "stageIndex": i,
                    "stageName": stage["stage"],
                    "matchStrength": stage_match_count,
                    "dangerLevel": "early" if i < 2 else "mid" if i < 4 else "critical"
                })
                total_danger += stage_match_count * (i + 1)  # Later stages score higher danger
        
        if matched_stages:
            # Calculate danger percentage based on how deep into the failure path they are
            max_possible = sum((i + 1) * 3 for i in range(len(startup["stages"])))
            danger_pct = min(100, round((total_danger / max_possible) * 100 * 2))
            
            matches.append({
                "name": startup["name"],
                "icon": startup["icon"],
                "raised": startup["raised"],
                "lifespan": startup["lifespan"],
                "deathCause": startup["death_cause"],
                "matchedStages": matched_stages,
                "dangerScore": danger_pct,
                "lesson": startup["lesson"],
                "survivalAdvice": startup["what_they_should_have_done"],
                "totalStages": len(startup["stages"]),
                "matchedCount": len(matched_stages)
            })
    
    # Sort by danger score (highest danger first)
    matches.sort(key=lambda x: x["dangerScore"], reverse=True)
    
    return matches[:5]  # Return top 5 matches

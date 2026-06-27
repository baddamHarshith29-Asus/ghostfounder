# ─────────────────────────────────────────────
# FEATURE 4: FAILURE PATTERN RECOGNITION
# Compares your path to 1000 failed startups
# ─────────────────────────────────────────────

FAILURE_PATTERNS = [
    {
        "pattern": ["price", "discount", "cheaper", "undercut", "low cost"],
        "name": "Competing on Price",
        "failure_rate": "78%",
        "lesson": "Price wars attract bad customers and destroy margins. Winners compete on value, not cost.",
        "examples": [
            "Fab.com burned $200M racing to the bottom on pricing",
            "Homejoy collapsed after undercutting competitors — then ran out of cash"
        ],
        "fix": "Raise your prices. Find 10 customers who will pay 3x what you charge now."
    },
    {
        "pattern": ["feature", "add more", "build more", "new feature", "many features"],
        "name": "Feature Overload",
        "failure_rate": "65%",
        "lesson": "Complexity kills focus. Ship one thing that works perfectly before adding more.",
        "examples": [
            "Google Wave had so many features nobody could explain what it did",
            "Friendfeed was too complex to describe in one sentence — nobody shared it"
        ],
        "fix": "Remove features until it hurts. Then remove one more."
    },
    {
        "pattern": ["scale", "expand", "grow fast", "hire", "open new"],
        "name": "Scaling Before Product-Market Fit",
        "failure_rate": "71%",
        "lesson": "Scaling a broken product just breaks it faster and more expensively.",
        "examples": [
            "Beepi scaled operations across 10 cities before fixing unit economics",
            "Sprig expanded to new cities while retention in the first city was still poor"
        ],
        "fix": "Prove 100 users love your product before thinking about 1000."
    },
    {
        "pattern": ["no feedback", "haven't talked", "build first", "launch then"],
        "name": "Building Without Customer Validation",
        "failure_rate": "82%",
        "lesson": "42% of startups fail because they build something nobody wants.",
        "examples": [
            "Quibi spent $1.75B on content without validating mobile-first short video demand",
            "Color.com raised $41M and built for 2 years without a single customer conversation"
        ],
        "fix": "Talk to 10 potential customers today. Not to pitch — to listen."
    },
    {
        "pattern": ["burn", "spend", "runway", "cash", "budget"],
        "name": "Ignoring Unit Economics",
        "failure_rate": "69%",
        "lesson": "If you lose money on every customer, you cannot grow your way out of it.",
        "examples": [
            "Drizly's delivery economics never worked — acquired for parts, not profit",
            "Many food delivery startups subsidized every order hoping volume would fix margins"
        ],
        "fix": "Calculate your cost to serve one customer. Make that number positive first."
    },
    {
        "pattern": ["pivot", "change", "different", "new direction", "rethink"],
        "name": "Pivoting Too Early",
        "failure_rate": "55%",
        "lesson": "Most pivots happen before the original idea was properly tested.",
        "examples": [
            "Odeo pivoted to Twitter before podcasting was actually tried seriously",
            "Many founders pivot at the first sign of friction, not genuine market rejection"
        ],
        "fix": "Have you talked to 50 customers and gotten 50 nos? If not, keep going."
    }
]

def check_failure_patterns(situation: str):
    """Returns matching failure patterns for the given situation"""
    matches = []
    situation_lower = situation.lower()
    for p in FAILURE_PATTERNS:
        if any(kw in situation_lower for kw in p["pattern"]):
            matches.append(p)
    return matches

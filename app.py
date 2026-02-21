import os
import random
from flask import Flask, render_template, request, jsonify, session

app = Flask(__name__)
app.secret_key = "startup-battlefield-mvp-secret-key-2026"

INITIAL_METRICS = {
    "cash": 70,
    "growth": 50,
    "reputation": 60,
    "morale": 75,
    "burn_rate": 15,
    "investor_sentiment": 60,
}

EVENTS = {
    "AI & Machine Learning": [
        {
            "headline": "GPU Cloud Costs Skyrocket Overnight",
            "narrative": "Your primary cloud provider just tripled GPU instance pricing. Training runs that cost $500 now cost $1500. Your burn rate is about to explode and investors are watching closely.",
            "event_type": "crisis",
            "icon": "🔥",
            "options": [
                {"id": 1, "title": "Switch to cheaper provider", "description": "Migrate workloads to a budget cloud provider with slower but affordable GPUs.", "risk_level": "Low", "hint": "Saves cash but may slow development", "icon": "💰",
                 "outcome": {"summary": "Migration took a week but saved significant costs. Some model training slowed down.", "tone": "mixed", "changes": {"cash": 5, "growth": -5, "reputation": 0, "morale": -3, "burn_rate": -8, "investor_sentiment": 5}, "ticker": "Startup pivots to budget cloud — cost efficiency lauded by board"}},
                {"id": 2, "title": "Build own GPU cluster", "description": "Invest heavily in purchasing your own hardware to eliminate recurring cloud costs.", "risk_level": "High", "hint": "Huge upfront cost, long-term savings possible", "icon": "🖥️",
                 "outcome": {"summary": "Massive upfront spend drained cash reserves, but you now own your compute. Investors are split.", "tone": "negative", "changes": {"cash": -25, "growth": 3, "reputation": 5, "morale": 5, "burn_rate": -12, "investor_sentiment": -8}, "ticker": "Bold infrastructure bet raises eyebrows on Sand Hill Road"}},
                {"id": 3, "title": "Negotiate enterprise deal", "description": "Leverage your growing usage to negotiate a long-term discount contract.", "risk_level": "Medium", "hint": "Could lock in savings or lock you into bad terms", "icon": "🤝",
                 "outcome": {"summary": "Secured a 40% discount but locked into a 2-year contract. Flexibility reduced but costs stabilized.", "tone": "positive", "changes": {"cash": 3, "growth": 0, "reputation": 3, "morale": 5, "burn_rate": -5, "investor_sentiment": 8}, "ticker": "Strategic cloud partnership secures runway extension"}},
            ],
            "rival": {"rival_name": "DeepMind Jr.", "rival_tagline": "Democratizing AGI", "rival_cash": 65, "rival_growth": 55, "rival_reputation": 58, "rival_action": "Just raised a $5M seed round from Sequoia.", "market_share_player": 52, "market_share_rival": 48},
        },
        {
            "headline": "Star Engineer Poached By Big Tech",
            "narrative": "Your lead ML engineer just got an offer from Google DeepMind — double the salary, full benefits, and stock options. They're giving you 48 hours to counter-offer or they walk.",
            "event_type": "crisis",
            "icon": "🚨",
            "options": [
                {"id": 1, "title": "Match the offer", "description": "Counter with a competitive salary raise and additional equity to retain your top talent.", "risk_level": "Medium", "hint": "Keeps talent but sets expensive precedent", "icon": "💸",
                 "outcome": {"summary": "Engineer stayed but the salary bump raised expectations across the entire team.", "tone": "mixed", "changes": {"cash": -10, "growth": 3, "reputation": 2, "morale": 8, "burn_rate": 5, "investor_sentiment": -3}, "ticker": "Key talent retained with aggressive counter-offer package"}},
                {"id": 2, "title": "Let them go gracefully", "description": "Wish them well, document their work, and begin recruiting a replacement.", "risk_level": "Low", "hint": "Saves money but loses expertise and momentum", "icon": "👋",
                 "outcome": {"summary": "The departure slowed your roadmap by 3 weeks. Morale dipped but you saved on burn.", "tone": "negative", "changes": {"cash": 5, "growth": -10, "reputation": -3, "morale": -12, "burn_rate": -3, "investor_sentiment": -5}, "ticker": "Key departure sends ripples through engineering team"}},
                {"id": 3, "title": "Promote from within", "description": "Promote a promising junior engineer and invest in their rapid upskilling.", "risk_level": "Medium", "hint": "Boosts culture but risky on execution speed", "icon": "⬆️",
                 "outcome": {"summary": "The junior rose to the challenge. Team morale soared from the internal promotion story.", "tone": "positive", "changes": {"cash": -2, "growth": -3, "reputation": 5, "morale": 12, "burn_rate": 0, "investor_sentiment": 3}, "ticker": "Internal promotion sparks culture-first narrative in tech press"}},
            ],
            "rival": {"rival_name": "NeuralNova", "rival_tagline": "AI for the real world", "rival_cash": 60, "rival_growth": 60, "rival_reputation": 55, "rival_action": "Launched a viral demo on X that got 2M views.", "market_share_player": 50, "market_share_rival": 50},
        },
        {
            "headline": "Viral Demo Explodes On Social Media",
            "narrative": "A user posted your AI product demo on Twitter/X and it went mega-viral — 5 million views in 24 hours. Your servers are melting, support inbox is flooded, and VCs are calling.",
            "event_type": "opportunity",
            "icon": "🚀",
            "options": [
                {"id": 1, "title": "Scale servers immediately", "description": "Throw money at infrastructure to handle the surge and capitalize on the moment.", "risk_level": "Medium", "hint": "Expensive but captures the wave", "icon": "⚡",
                 "outcome": {"summary": "Scaled up just in time. Converted 15% of viral traffic into signups. Burn rate spiked but growth exploded.", "tone": "positive", "changes": {"cash": -12, "growth": 20, "reputation": 15, "morale": 10, "burn_rate": 8, "investor_sentiment": 15}, "ticker": "Viral moment captured — user signups surge 400% overnight"}},
                {"id": 2, "title": "Add waitlist and hype", "description": "Put up a waitlist page to create exclusivity and manage the load carefully.", "risk_level": "Low", "hint": "Builds FOMO but might lose the momentum", "icon": "📋",
                 "outcome": {"summary": "Waitlist hit 50K signups. The exclusivity created massive buzz but some users went to competitors.", "tone": "positive", "changes": {"cash": 2, "growth": 10, "reputation": 12, "morale": 8, "burn_rate": 0, "investor_sentiment": 10}, "ticker": "50K waitlist signups fuel investor FOMO — Series A talks begin"}},
                {"id": 3, "title": "Ignore it, stay focused", "description": "Don't chase vanity metrics. Keep building the core product for paying customers.", "risk_level": "Low", "hint": "Disciplined but may waste a once-in-a-lifetime moment", "icon": "🎯",
                 "outcome": {"summary": "The viral wave passed. You stayed focused but competitors captured the market attention.", "tone": "negative", "changes": {"cash": 0, "growth": -5, "reputation": -8, "morale": 3, "burn_rate": 0, "investor_sentiment": -10}, "ticker": "Missed viral window — analysts question growth strategy"}},
            ],
            "rival": {"rival_name": "CortexAI", "rival_tagline": "Think faster", "rival_cash": 70, "rival_growth": 45, "rival_reputation": 62, "rival_action": "Quietly acquired a small data labeling startup.", "market_share_player": 55, "market_share_rival": 45},
        },
        {
            "headline": "Co-founder Wants To Pivot Direction",
            "narrative": "Your technical co-founder wants to abandon B2B and pivot to consumer AI. They believe the real money is in a ChatGPT competitor. The board meeting is tomorrow and tensions are high.",
            "event_type": "neutral",
            "icon": "⚖️",
            "options": [
                {"id": 1, "title": "Support the pivot fully", "description": "Back your co-founder and rewrite the roadmap toward consumer AI.", "risk_level": "High", "hint": "Could find a massive market or destroy current traction", "icon": "🔄",
                 "outcome": {"summary": "The pivot energized the team but existing B2B customers churned. Starting from scratch in consumer.", "tone": "mixed", "changes": {"cash": -8, "growth": -15, "reputation": -5, "morale": 10, "burn_rate": 5, "investor_sentiment": -12}, "ticker": "Bold pivot to consumer AI divides the startup community"}},
                {"id": 2, "title": "Reject and stay course", "description": "Firmly stick with the B2B strategy and ask your co-founder to align.", "risk_level": "Medium", "hint": "Maintains focus but risks co-founder conflict", "icon": "🛡️",
                 "outcome": {"summary": "Co-founder grudgingly agreed but the relationship is strained. Product focus remained sharp.", "tone": "mixed", "changes": {"cash": 0, "growth": 5, "reputation": 3, "morale": -8, "burn_rate": 0, "investor_sentiment": 5}, "ticker": "Internal tensions surface as leadership holds firm on strategy"}},
                {"id": 3, "title": "Compromise with a skunkworks", "description": "Let the co-founder run a small side team to prototype the consumer idea with a tight budget.", "risk_level": "Low", "hint": "Keeps everyone happy but splits focus slightly", "icon": "🧪",
                 "outcome": {"summary": "The skunkworks produced a promising prototype. Main product stayed on track. Team felt heard.", "tone": "positive", "changes": {"cash": -5, "growth": 2, "reputation": 5, "morale": 10, "burn_rate": 3, "investor_sentiment": 5}, "ticker": "Innovation lab approach praised — startup balances vision with execution"}},
            ],
            "rival": {"rival_name": "SynthMind", "rival_tagline": "Synthetic intelligence, real results", "rival_cash": 55, "rival_growth": 50, "rival_reputation": 60, "rival_action": "Just pivoted to enterprise — stealing your leads.", "market_share_player": 48, "market_share_rival": 52},
        },
        {
            "headline": "Acquisition Offer Lands On Your Desk",
            "narrative": "A Fortune 500 tech company just offered $20M to acquire your startup. The offer expires in 72 hours. Your investors are excited but your team is terrified of being absorbed.",
            "event_type": "opportunity",
            "icon": "💎",
            "options": [
                {"id": 1, "title": "Accept the acquisition", "description": "Take the guaranteed exit and reward your investors and early employees.", "risk_level": "Low", "hint": "Safe exit but your independent journey ends", "icon": "✅",
                 "outcome": {"summary": "Deal closed. Investors celebrated, team got payouts, but your startup brand dissolved into the acquirer.", "tone": "positive", "changes": {"cash": 30, "growth": -10, "reputation": 10, "morale": -5, "burn_rate": -10, "investor_sentiment": 25}, "ticker": "BREAKING: Acquisition deal closes — founder exits with $20M payout"}},
                {"id": 2, "title": "Reject and go big", "description": "Turn down the offer and bet on building a billion-dollar company independently.", "risk_level": "High", "hint": "Massive upside if you succeed, massive risk if you don't", "icon": "🎰",
                 "outcome": {"summary": "The rejection made headlines. VCs took notice of your confidence but the pressure is now immense.", "tone": "mixed", "changes": {"cash": 0, "growth": 8, "reputation": 12, "morale": 8, "burn_rate": 0, "investor_sentiment": -5}, "ticker": "Founder rejects $20M offer — betting on unicorn status"}},
                {"id": 3, "title": "Counter with partnership", "description": "Propose a strategic partnership instead of acquisition — keep independence but gain resources.", "risk_level": "Medium", "hint": "Best of both worlds if they agree", "icon": "🤝",
                 "outcome": {"summary": "They agreed to a $3M strategic investment plus distribution deal. Independence preserved with added firepower.", "tone": "positive", "changes": {"cash": 15, "growth": 8, "reputation": 8, "morale": 10, "burn_rate": -2, "investor_sentiment": 12}, "ticker": "Strategic partnership deal lands — startup keeps autonomy with corporate backing"}},
            ],
            "rival": {"rival_name": "AlphaForge", "rival_tagline": "Forge the future", "rival_cash": 50, "rival_growth": 65, "rival_reputation": 70, "rival_action": "Got rejected by the same acquirer. Scrambling for runway.", "market_share_player": 54, "market_share_rival": 46},
        },
    ],
    "_default": [
        {
            "headline": "Key Client Threatens To Leave",
            "narrative": "Your biggest client (30% of revenue) is unhappy with recent product bugs and is evaluating a competitor. You have one week to turn this around or lose them for good.",
            "event_type": "crisis",
            "icon": "😰",
            "options": [
                {"id": 1, "title": "Emergency bug fix sprint", "description": "Pull the entire engineering team into a week-long crunch to fix all reported issues.", "risk_level": "Medium", "hint": "May fix client but burns out the team", "icon": "🔧",
                 "outcome": {"summary": "Bugs fixed in 5 days. Client impressed by responsiveness but team is exhausted.", "tone": "mixed", "changes": {"cash": -3, "growth": 5, "reputation": 8, "morale": -10, "burn_rate": 2, "investor_sentiment": 5}, "ticker": "Crisis averted — major client renews after emergency response"}},
                {"id": 2, "title": "Offer a huge discount", "description": "Give the client 50% off for 6 months to buy time while you fix things.", "risk_level": "Low", "hint": "Keeps them short-term but hurts revenue", "icon": "🏷️",
                 "outcome": {"summary": "Client stayed but the discount set a bad precedent. Other clients heard and want deals too.", "tone": "negative", "changes": {"cash": -8, "growth": -3, "reputation": -5, "morale": 0, "burn_rate": 3, "investor_sentiment": -5}, "ticker": "Discount strategy backfires as other clients demand equal treatment"}},
                {"id": 3, "title": "Let them go, diversify", "description": "Accept the loss and accelerate efforts to sign three smaller clients.", "risk_level": "High", "hint": "Risky revenue hit but healthier long-term", "icon": "🎯",
                 "outcome": {"summary": "Lost 30% of revenue overnight but signed two new clients within the month. Healthier pipeline.", "tone": "mixed", "changes": {"cash": -12, "growth": 8, "reputation": 3, "morale": 5, "burn_rate": 0, "investor_sentiment": -3}, "ticker": "Revenue diversification play — bold move or desperate gamble?"}},
            ],
            "rival": {"rival_name": "VeloTech", "rival_tagline": "Speed matters", "rival_cash": 60, "rival_growth": 55, "rival_reputation": 50, "rival_action": "Just launched a competing feature targeting your niche.", "market_share_player": 50, "market_share_rival": 50},
        },
        {
            "headline": "Regulatory Compliance Deadline Looms",
            "narrative": "New government regulations require expensive compliance changes by next month. Non-compliance means massive fines and potential shutdown. Your legal team is panicking.",
            "event_type": "crisis",
            "icon": "⚖️",
            "options": [
                {"id": 1, "title": "Hire compliance consultants", "description": "Bring in expensive experts to fast-track your compliance overhaul.", "risk_level": "Low", "hint": "Safe but costly", "icon": "👔",
                 "outcome": {"summary": "Compliance achieved on time. Expensive but avoided any legal issues. Investors relieved.", "tone": "positive", "changes": {"cash": -15, "growth": 0, "reputation": 5, "morale": 3, "burn_rate": 2, "investor_sentiment": 8}, "ticker": "Full compliance achieved ahead of deadline — clean bill of health"}},
                {"id": 2, "title": "Do minimal compliance", "description": "Meet the bare minimum requirements and hope for the best.", "risk_level": "High", "hint": "Saves money but regulators may come knocking", "icon": "🎲",
                 "outcome": {"summary": "Passed initial inspection but regulators flagged concerns. You're on a watchlist now.", "tone": "mixed", "changes": {"cash": -3, "growth": 0, "reputation": -8, "morale": -5, "burn_rate": 0, "investor_sentiment": -5}, "ticker": "Regulatory watchlist placement sends warning signals to market"}},
                {"id": 3, "title": "Lobby for exemption", "description": "Join an industry coalition to lobby for startup exemptions from the new rules.", "risk_level": "Medium", "hint": "Could pay off big or waste time and money", "icon": "🏛️",
                 "outcome": {"summary": "The coalition got a 6-month extension for startups under 50 employees. Major win!", "tone": "positive", "changes": {"cash": -5, "growth": 3, "reputation": 10, "morale": 8, "burn_rate": 0, "investor_sentiment": 10}, "ticker": "Industry coalition wins regulatory reprieve — startup sector celebrates"}},
            ],
            "rival": {"rival_name": "ComplianceFirst", "rival_tagline": "Trust built in", "rival_cash": 55, "rival_growth": 40, "rival_reputation": 70, "rival_action": "Already fully compliant — marketing it as a competitive advantage.", "market_share_player": 48, "market_share_rival": 52},
        },
        {
            "headline": "Surprise Product Hunt Launch Goes Viral",
            "narrative": "An employee accidentally posted your beta on Product Hunt and it's trending #1. Thousands of users are signing up but the product isn't ready for this kind of attention.",
            "event_type": "opportunity",
            "icon": "🎉",
            "options": [
                {"id": 1, "title": "Ride the wave hard", "description": "Go all-in on the accidental launch — spin up support, fix critical bugs, capitalize.", "risk_level": "Medium", "hint": "Maximum growth potential but risky with unfinished product", "icon": "🏄",
                 "outcome": {"summary": "Captured 8,000 signups. Some users hit bugs but overall sentiment was positive. Exhausting week.", "tone": "positive", "changes": {"cash": -5, "growth": 18, "reputation": 10, "morale": -5, "burn_rate": 3, "investor_sentiment": 12}, "ticker": "Accidental Product Hunt launch becomes legendary origin story"}},
                {"id": 2, "title": "Take it down immediately", "description": "Remove the listing and issue an apology — maintain quality control.", "risk_level": "Low", "hint": "Protects brand but kills organic momentum", "icon": "🚫",
                 "outcome": {"summary": "The takedown was noticed. Some praised the quality focus, others called it a missed opportunity.", "tone": "mixed", "changes": {"cash": 0, "growth": -5, "reputation": 3, "morale": 5, "burn_rate": 0, "investor_sentiment": -3}, "ticker": "Product Hunt takedown sparks debate — quality vs. opportunity"}},
                {"id": 3, "title": "Pivot to invite-only beta", "description": "Keep the hype but convert it into an exclusive invite-only program.", "risk_level": "Low", "hint": "Creates scarcity and manages quality", "icon": "🔑",
                 "outcome": {"summary": "The invite-only approach created massive FOMO. 20K people on the waitlist. Press coverage followed.", "tone": "positive", "changes": {"cash": 0, "growth": 12, "reputation": 15, "morale": 8, "burn_rate": 0, "investor_sentiment": 10}, "ticker": "Invite-only beta creates massive demand — VCs lining up for meetings"}},
            ],
            "rival": {"rival_name": "QuickShip", "rival_tagline": "Ship fast, learn faster", "rival_cash": 65, "rival_growth": 50, "rival_reputation": 55, "rival_action": "Tried to launch on Product Hunt same day — got overshadowed by you.", "market_share_player": 55, "market_share_rival": 45},
        },
        {
            "headline": "Team Burnout Reaches Critical Levels",
            "narrative": "Three senior engineers just submitted PTO requests for the same two weeks. Anonymous Glassdoor reviews mention 'toxic crunch culture'. Your team is breaking.",
            "event_type": "crisis",
            "icon": "😴",
            "options": [
                {"id": 1, "title": "Mandatory company retreat", "description": "Shut down for a week, take everyone on a paid retreat to reset and recharge.", "risk_level": "Medium", "hint": "Great for morale but delays everything", "icon": "🏖️",
                 "outcome": {"summary": "The retreat was transformative. Team came back energized and more bonded than ever. Lost a week of shipping.", "tone": "positive", "changes": {"cash": -8, "growth": -5, "reputation": 8, "morale": 20, "burn_rate": 0, "investor_sentiment": 0}, "ticker": "Company retreat resets culture — Glassdoor rating jumps to 4.5 stars"}},
                {"id": 2, "title": "Hire more to spread load", "description": "Immediately post 5 new positions to reduce per-person workload.", "risk_level": "Medium", "hint": "More hands but hiring takes time and money", "icon": "👥",
                 "outcome": {"summary": "Hired 3 of 5 roles within a month. Workload improved but onboarding was chaotic.", "tone": "mixed", "changes": {"cash": -12, "growth": 3, "reputation": 3, "morale": 8, "burn_rate": 8, "investor_sentiment": 0}, "ticker": "Hiring spree underway — team expansion signals growth to market"}},
                {"id": 3, "title": "Push through the crunch", "description": "Deny the PTO, set a sprint goal, and promise bonuses after the deadline.", "risk_level": "High", "hint": "Might ship faster but could trigger resignations", "icon": "💪",
                 "outcome": {"summary": "Two engineers quit. The remaining team is resentful. You shipped the feature but at enormous human cost.", "tone": "negative", "changes": {"cash": 2, "growth": 8, "reputation": -12, "morale": -20, "burn_rate": -2, "investor_sentiment": 3}, "ticker": "Engineering exodus after forced crunch — culture crisis deepens"}},
            ],
            "rival": {"rival_name": "ChillStack", "rival_tagline": "Work smart, not hard", "rival_cash": 70, "rival_growth": 45, "rival_reputation": 65, "rival_action": "Just announced 4-day work weeks and got massive press coverage.", "market_share_player": 47, "market_share_rival": 53},
        },
        {
            "headline": "Investor Demands Board Seat",
            "narrative": "Your lead investor is threatening to pull follow-on funding unless they get a board seat with veto power. This could mean losing control of your own company.",
            "event_type": "neutral",
            "icon": "🪑",
            "options": [
                {"id": 1, "title": "Grant the board seat", "description": "Give the investor what they want to secure continued funding.", "risk_level": "Low", "hint": "Secures cash but you lose some control", "icon": "🤝",
                 "outcome": {"summary": "Funding secured. Investor added helpful connections but now has veto power on key decisions.", "tone": "mixed", "changes": {"cash": 15, "growth": 3, "reputation": 0, "morale": -5, "burn_rate": 0, "investor_sentiment": 12}, "ticker": "Governance change secures funding — founder control diluted"}},
                {"id": 2, "title": "Refuse and find new investors", "description": "Reject the demand and start courting alternative investors immediately.", "risk_level": "High", "hint": "Keeps control but fundraising is brutal", "icon": "🚪",
                 "outcome": {"summary": "Original investor badmouthed you to other VCs. Fundraising got harder but you found an angel who believes in you.", "tone": "mixed", "changes": {"cash": -5, "growth": 0, "reputation": -5, "morale": 8, "burn_rate": 0, "investor_sentiment": -15}, "ticker": "Founder-investor split sends shockwaves through VC community"}},
                {"id": 3, "title": "Negotiate observer seat", "description": "Offer a board observer role with no voting rights as a compromise.", "risk_level": "Medium", "hint": "Diplomatic middle ground", "icon": "👁️",
                 "outcome": {"summary": "Investor accepted the observer role. Relationship preserved, funding continued with slight tension.", "tone": "positive", "changes": {"cash": 8, "growth": 2, "reputation": 5, "morale": 3, "burn_rate": 0, "investor_sentiment": 8}, "ticker": "Diplomatic compromise keeps investor relationship intact"}},
            ],
            "rival": {"rival_name": "FundedFast", "rival_tagline": "Move fast with money", "rival_cash": 80, "rival_growth": 55, "rival_reputation": 45, "rival_action": "Just closed a Series A — now has 3x your runway.", "market_share_player": 45, "market_share_rival": 55},
        },
    ],
}


def clamp(value, lo=0, hi=100):
    return max(lo, min(hi, int(value)))


def pick_event(industry, round_num, used_indices):
    pool = EVENTS.get(industry, EVENTS["_default"])
    available = [i for i in range(len(pool)) if i not in used_indices]
    if not available:
        available = list(range(len(pool)))
    idx = random.choice(available)
    return idx, pool[idx]


def generate_final(metrics, history):
    avg = (metrics["cash"] + metrics["growth"] + metrics["reputation"] + metrics["morale"] + metrics["investor_sentiment"]) / 5
    if avg >= 75:
        verdict, grade = "UNICORN", "S"
        headline = "The Next Tech Titan Is Born"
        narrative = f"Against all odds, your startup conquered every challenge thrown its way. Investors are fighting over your Series B, users are raving, and the press can't stop writing about you. You've built something truly extraordinary."
    elif avg >= 60:
        verdict, grade = "ACQUIRED", "A"
        headline = "Big Tech Comes Knocking With A Check"
        narrative = f"Your consistent performance caught the eye of a major acquirer. After intense negotiations, you secured a deal that rewarded your team and investors handsomely. A proud exit."
    elif avg >= 45:
        verdict, grade = "SURVIVED", "B"
        headline = "Still Standing — Against The Odds"
        narrative = f"It wasn't glamorous, but you survived. Your startup is still running, still growing, and still fighting. Most startups don't make it this far. That counts for something."
    elif avg >= 30:
        verdict, grade = "SURVIVED", "C"
        headline = "Barely Hanging On By A Thread"
        narrative = f"Your startup limps forward, battered by crises and tough decisions. Revenue is thin, morale is shaky, but you're technically still alive. The next quarter will be make-or-break."
    elif avg >= 15:
        verdict, grade = "SHUTDOWN", "D"
        headline = "The Dream Fades To Black"
        narrative = f"Too many bad decisions, too little runway. Your startup couldn't find product-market fit in time. The team dispersed, investors wrote it off, and the domain name expired."
    else:
        verdict, grade = "BANKRUPT", "F"
        headline = "Total Collapse — Lights Out"
        narrative = f"Cash hit zero, team walked out, investors sued. Every possible thing that could go wrong did. This is the cautionary tale other founders will study."

    score = int(min(100, max(0, avg * 1.2)))
    advice_pool = [
        "Cash is oxygen — never forget that.",
        "Your team is your product. Treat them accordingly.",
        "Speed beats perfection in the early days.",
        "Listen to customers, not just investors.",
        "The best founders adapt without losing their vision.",
    ]
    return {
        "verdict": verdict,
        "headline": headline,
        "narrative": narrative,
        "final_score": score,
        "grade": grade,
        "advice": random.choice(advice_pool),
    }


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/start", methods=["POST"])
def start_game():
    data = request.json
    startup_info = {
        "name": data.get("name", "My Startup"),
        "industry": data.get("industry", "Technology"),
    }
    game_state = {
        "startup_info": startup_info,
        "metrics": dict(INITIAL_METRICS),
        "round": 1,
        "history": [],
        "alive": True,
        "used_events": [],
    }
    session["game"] = game_state
    return jsonify({"status": "ok", "game_state": game_state})


@app.route("/api/event", methods=["POST"])
def get_event():
    game = session.get("game")
    if not game or not game["alive"]:
        return jsonify({"error": "No active game"}), 400

    idx, event_data = pick_event(
        game["startup_info"]["industry"],
        game["round"],
        game.get("used_events", []),
    )
    game.setdefault("used_events", []).append(idx)

    clean_options = []
    for opt in event_data["options"]:
        clean_options.append({
            "id": opt["id"],
            "title": opt["title"],
            "description": opt["description"],
            "risk_level": opt["risk_level"],
            "hint": opt["hint"],
            "icon": opt["icon"],
        })

    event = {
        "headline": event_data["headline"],
        "narrative": event_data["narrative"],
        "event_type": event_data["event_type"],
        "icon": event_data["icon"],
        "options": clean_options,
    }
    rival = event_data.get("rival")

    session["current_event_data"] = event_data
    session["current_event"] = event
    session.modified = True

    return jsonify({"event": event, "rival": rival, "round": game["round"]})


@app.route("/api/decide", methods=["POST"])
def make_decision():
    game = session.get("game")
    event_data = session.get("current_event_data")
    event = session.get("current_event")
    if not game or not event_data:
        return jsonify({"error": "No active game or event"}), 400

    data = request.json
    option_id = data.get("option_id", 1)

    chosen = None
    for opt in event_data["options"]:
        if opt["id"] == option_id:
            chosen = opt
            break
    if not chosen:
        chosen = event_data["options"][0]

    outcome_data = chosen["outcome"]
    changes = dict(outcome_data["changes"])

    fuzz = random.randint(-3, 3)
    for key in changes:
        changes[key] = changes[key] + random.randint(-2, 2)

    outcome = {
        "outcome_summary": outcome_data["summary"],
        "outcome_tone": outcome_data["tone"],
        "metric_changes": changes,
        "news_ticker": outcome_data["ticker"],
    }

    old_metrics = dict(game["metrics"])
    for key in game["metrics"]:
        if key in changes:
            game["metrics"][key] = clamp(game["metrics"][key] + changes[key])

    game["history"].append({
        "round": game["round"],
        "event_headline": event["headline"],
        "chosen_option": chosen["title"],
        "outcome_summary": outcome["outcome_summary"],
        "metric_changes": changes,
    })

    if game["metrics"]["cash"] <= 0:
        game["alive"] = False

    game["round"] += 1
    is_final = game["round"] > 5 or not game["alive"]

    final_result = None
    if is_final:
        final_result = generate_final(game["metrics"], game["history"])

    session["game"] = game
    session["current_event"] = None
    session["current_event_data"] = None
    session.modified = True

    return jsonify({
        "outcome": outcome,
        "old_metrics": old_metrics,
        "new_metrics": game["metrics"],
        "metric_changes": changes,
        "is_final": is_final,
        "alive": game["alive"],
        "final_result": final_result,
        "round": game["round"],
    })


@app.route("/api/reset", methods=["POST"])
def reset_game():
    session.clear()
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=True, port=5000)

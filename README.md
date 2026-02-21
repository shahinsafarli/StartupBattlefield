# Startup Battlefield Simulator

A cinematic, turn-based startup simulation game powered by Google Gemini AI. Play as a startup founder navigating 5 rounds of crises, opportunities, and pivotal decisions — with AI-generated events tailored to YOUR specific startup idea.

---

## Features

- **AI-Powered Events**: Gemini generates unique crisis/opportunity scenarios based on your startup
- **AI Scoring**: Real AI-based outcome evaluation — no fake scores or predefined results
- **User-Specific**: Enter YOUR startup idea and get tailored scenarios, options, and outcomes
- **Cyberpunk UI**: Dark mode, animated bars, glitch effects, screen shakes, news tickers
- **Rival System**: AI-generated rival startup competes against you with market share wars
- **5-Round Campaign**: Each round escalates — from early-stage crisis to endgame pivot-or-scale
- **Visual Effects**: Red glitch on cash drops, green flash on growth spikes, screen shake on crises
- **Final Verdict**: AI judges your entire journey with a grade (S/A/B/C/D/F) and dramatic narrative

---

## Prerequisites

- **Python 3.8+** installed on your system
- **Google Gemini API Key** (free tier) — get one at: https://aistudio.google.com/app/apikey

---

## Step-by-Step Setup Instructions

### Step 1: Open Terminal

Open PowerShell or Command Prompt and navigate to the project folder:

```bash
cd C:\Users\User\Desktop\proje
```

### Step 2: Create a Virtual Environment

```bash
python -m venv venv
```

### Step 3: Activate the Virtual Environment

**Windows (PowerShell):**
```bash
.\venv\Scripts\Activate.ps1
```

If you get an execution policy error, run this first:
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Windows (CMD):**
```bash
venv\Scripts\activate.bat
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Set Your Gemini API Key

Open the `.env` file in the project root and replace the placeholder:

```
GEMINI_API_KEY=your_actual_api_key_here
```

**How to get a free Gemini API key:**
1. Go to https://aistudio.google.com/app/apikey
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key and paste it in `.env`

### Step 6: Run the Game

```bash
python app.py
```

### Step 7: Play!

Open your browser and go to:

```
http://127.0.0.1:5000
```

---

## How to Play

1. **Enter your startup details** — name, industry, and a brief description of your idea
2. **Click "Launch Simulation"** to begin
3. **Each round**: Read the AI-generated event, then choose one of three strategic options
4. **Watch your metrics** change based on AI-evaluated outcomes
5. **Survive 5 rounds** to get your final verdict and score

---

## Project Structure

```
proje/
├── app.py              # Flask backend + Gemini AI agent
├── requirements.txt    # Python dependencies
├── .env                # API key configuration
├── README.md           # This file
└── templates/
    └── index.html      # Full game UI (HTML/CSS/JS)
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError` | Make sure venv is activated and you ran `pip install -r requirements.txt` |
| API errors / 500 | Check your `.env` file has a valid Gemini API key |
| Execution policy error (PS) | Run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` |
| Port 5000 in use | Change port in `app.py`: `app.run(debug=True, port=5001)` |

---

## Tech Stack

- **Backend**: Python / Flask
- **AI Engine**: Google Gemini 2.0 Flash (free tier)
- **Frontend**: Vanilla HTML/CSS/JS (no build tools needed)
- **Fonts**: Orbitron (headings), Inter (body), JetBrains Mono (data)

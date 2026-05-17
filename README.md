<<<<<<< HEAD
# 🏏 Captain Cool — IPL Multi-Agent Match Strategist

> **Built on Google Gemini · APL GDG Pune Hackathon 2025**

A production-grade agentic AI system that acts as a virtual IPL captain, making the next tactical decision in a live match the way **Dhoni, Rohit, or Hardik** would — powered entirely by **Google Gemini 2.5 Flash**.

---

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────────┐
│               Captain Cool — 5-Turn Debate               │
│                                                          │
│  📊 Stats Analyst  →  Real function calling              │
│     ↓ Stats Report (live weather + player stats)         │
│  🧠 Strategist v1  →  Proposes tactical call             │
│     ↓                                                    │
│  😈 Devil's Advocate → Challenges the call               │
│     ↓                                                    │
│  🧠 Strategist v2  →  Revises or defends                 │
│     ↓                                                    │
│  🎙️ Commentator    →  Fan-friendly final verdict          │
└──────────────────────────────────────────────────────────┘
```

### The 4 Named Agents

| Agent | Role | Gemini Feature |
|-------|------|----------------|
| 📊 **Stats Analyst** | Data gatherer | **Function calling** — Live weather API, player stats, win probability |
| 🧠 **Strategist** | Captain brain | Dhoni/Rohit/Hardik persona system prompts |
| 😈 **Devil's Advocate** | Contrarian challenger | Independent Gemini call to pressure-test the strategy |
| 🎙️ **Commentator** | Fan-friendly synthesizer | Confidence score + counterfactual analysis |

---

## 🚀 Quick Start

### 1. Clone & set up environment
```bash
cd APL_GDG_Pune
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY from https://aistudio.google.com/apikey
```

### 2. Install dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 3. Run the server
```bash
cd backend
python main.py
# OR: uvicorn main:app --reload --port 8000
```

### 4. Open the app
Navigate to **http://localhost:8000** in your browser.

---

## 🛠️ Tech Stack

- **Gemini API**: `gemini-2.5-flash` via `google-genai` Python SDK
- **Function Calling**: Stats Analyst uses 5 real tool calls (weather API, player stats, head-to-head, venue data, win probability)
- **Real-time streaming**: SSE (Server-Sent Events) for live debate updates
- **Backend**: FastAPI + Python async
- **Frontend**: Vanilla HTML/CSS/JS — dark stadium aesthetic

---

## 📁 Project Structure

```
APL_GDG_Pune/
├── backend/
│   ├── agents/
│   │   ├── stats_analyst.py    # Agent 1: Tool caller (function calling)
│   │   ├── strategist.py       # Agent 2: Captain brain (runs twice)
│   │   ├── devils_advocate.py  # Agent 3: Challenger
│   │   └── commentator.py      # Agent 4: Fan-friendly synthesis
│   ├── tools/
│   │   ├── weather_tool.py     # Live Open-Meteo API integration
│   │   ├── stats_tool.py       # IPL 2024-25 player database
│   │   └── win_probability.py  # Sigmoid win probability model
│   ├── orchestrator.py         # 5-turn debate loop + SSE events
│   ├── main.py                 # FastAPI server
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── app.js
├── .env.example
└── README.md
```

---

## 🏏 Sample Scenario

**Input**: MI vs CSK, 2nd innings, over 16.0, 145/3 chasing 187 at Wankhede with dew. Tim David on strike, Hardik at non-striker. Chahal has 2 overs left.

**Output**: 5-turn debate where the Strategist recommends Chahar over Chahal (dew makes legspin ineffective), the Devil's Advocate pushes back arguing Chahal's variations are the only wicket-taking option, the Strategist defends with dew data from the live weather API, and the Commentator wraps it in punchy Wankhede night cricket language with a 74% confidence score.

---

## 🔧 Requirements

- Python 3.11+
- A valid Gemini API key (free tier works): https://aistudio.google.com/apikey

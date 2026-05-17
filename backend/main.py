"""
Captain Cool — FastAPI Server
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Serves the frontend and exposes:
  POST /api/analyze  — starts a new debate (returns SSE stream)
  GET  /api/health   — health check
  GET  /             — serves index.html
"""

import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

# Load env from parent directory
load_dotenv(Path(__file__).parent.parent / ".env")

from orchestrator import create_orchestrator

app = FastAPI(
    title="Captain Cool — IPL Multi-Agent Strategist",
    description="A Gemini-powered multi-agent system that debates and decides cricket tactics like Dhoni, Rohit, or Hardik.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount frontend static files
frontend_dir = Path(__file__).parent.parent / "frontend"
if frontend_dir.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_dir)), name="static")


# ─── Request Model ────────────────────────────────────────────────────────────

class MatchState(BaseModel):
    innings: int = Field(default=2, ge=1, le=2)
    over: int = Field(default=16, ge=0, le=19)
    ball: int = Field(default=0, ge=0, le=5)
    current_score: int = Field(default=145, ge=0)
    wickets: int = Field(default=3, ge=0, le=10)
    target: int | None = Field(default=187)
    batting_team: str = Field(default="Mumbai Indians")
    bowling_team: str = Field(default="Chennai Super Kings")
    striker: str = Field(default="Tim David")
    striker_handedness: str = Field(default="Right-handed")
    non_striker: str = Field(default="Hardik Pandya")
    bowlers_used: dict = Field(default={"Deepak Chahar": 3, "Ravindra Jadeja": 3, "Yuzvendra Chahal": 2, "Tushar Deshpande": 2})
    bowlers_remaining: dict = Field(default={"Deepak Chahar": 1, "Yuzvendra Chahal": 2, "Tushar Deshpande": 2})
    venue: str = Field(default="Wankhede Stadium, Mumbai")
    pitch_type: str = Field(default="Flat")
    dew_factor: str = Field(default="Yes")
    impact_player_available: bool = Field(default=True)
    captain_style: str = Field(default="Dhoni")
    phase: str = Field(default="Death overs (17-20)")


# ─── Routes ───────────────────────────────────────────────────────────────────

@app.get("/")
async def serve_index():
    """Serve the frontend."""
    index_path = frontend_dir / "index.html"
    if index_path.exists():
        return FileResponse(str(index_path))
    return {"message": "Captain Cool API is running. Frontend not found."}


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    api_key = os.getenv("GEMINI_API_KEY")
    return {
        "status": "ok",
        "service": "Captain Cool — IPL Multi-Agent Strategist",
        "gemini_configured": bool(api_key and api_key != "your_gemini_api_key_here"),
        "model": os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
    }


@app.post("/api/analyze")
async def analyze_match(match_state: MatchState):
    """
    Start the multi-agent debate for the given match state.
    Returns a Server-Sent Events stream with debate progress.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "your_gemini_api_key_here":
        raise HTTPException(
            status_code=500,
            detail="GEMINI_API_KEY not configured. Please add it to your .env file.",
        )

    run_debate = create_orchestrator()
    state_dict = match_state.model_dump()

    async def event_stream():
        async for event in run_debate(state_dict):
            # Format as SSE
            yield f"event: {event['event']}\ndata: {json.dumps(event['data'])}\n\n"
        yield "event: end\ndata: {}\n\n"

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )


@app.get("/api/teams")
async def get_teams():
    """Get list of IPL teams for the frontend dropdowns."""
    return {
        "teams": [
            "Mumbai Indians",
            "Chennai Super Kings",
            "Royal Challengers Bengaluru",
            "Kolkata Knight Riders",
            "Rajasthan Royals",
            "Sunrisers Hyderabad",
            "Delhi Capitals",
            "Punjab Kings",
            "Gujarat Titans",
            "Lucknow Super Giants",
        ],
        "venues": [
            "Wankhede Stadium, Mumbai",
            "MA Chidambaram Stadium, Chennai",
            "Eden Gardens, Kolkata",
            "Arun Jaitley Stadium, Delhi",
            "M. Chinnaswamy Stadium, Bengaluru",
            "Rajiv Gandhi Intl Cricket Stadium, Hyderabad",
            "Sawai Mansingh Stadium, Jaipur",
            "BRSABV Ekana Cricket Stadium, Lucknow",
            "Punjab Cricket Association Stadium, Mohali",
            "Narendra Modi Stadium, Ahmedabad",
        ],
        "captain_styles": ["Dhoni", "Rohit", "Hardik"],
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )

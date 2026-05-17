"""
Orchestrator — Multi-Agent Debate Loop
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Coordinates the 5-turn agent debate:
  Turn 1: Stats Analyst (with real tool calls)
  Turn 2: Strategist proposes Decision v1
  Turn 3: Devil's Advocate challenges
  Turn 4: Strategist revises → Decision v2
  Turn 5: Commentator synthesizes → Final output

Yields Server-Sent Events (SSE) for real-time streaming to frontend.
"""

import asyncio
import json
import os
from typing import AsyncGenerator

from google import genai

from agents.stats_analyst import create_stats_analyst
from agents.strategist import create_strategist
from agents.devils_advocate import create_devils_advocate
from agents.commentator import create_commentator


def create_orchestrator():
    """Creates and returns the orchestrator function."""

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set")

    client = genai.Client(api_key=api_key)
    model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

    async def run_debate(match_state: dict) -> AsyncGenerator[dict, None]:
        """
        Runs the full multi-agent debate and yields SSE events.

        Yields dicts with:
          - event: SSE event name (e.g. "agent_start", "agent_done", "complete", "error")
          - data: Event payload
        """
        captain_style = match_state.get("captain_style", "Dhoni")

        try:
            # ── TURN 1: Stats Analyst ────────────────────────────────────────
            yield {
                "event": "agent_start",
                "data": {
                    "agent": "Stats Analyst",
                    "emoji": "📊",
                    "message": "Firing up the analytics engine — fetching live weather, player stats, and win probability...",
                    "turn": 1,
                    "total_turns": 5,
                },
            }

            analyze = create_stats_analyst(client, model)
            stats_result = await analyze(match_state)

            yield {
                "event": "agent_done",
                "data": {
                    "agent": "Stats Analyst",
                    "emoji": "📊",
                    "turn": 1,
                    "content": stats_result["report"],
                    "tool_calls": stats_result.get("tool_calls", []),
                    "label": "Stats Report",
                },
            }

            await asyncio.sleep(0.2)

            # ── TURN 2: Strategist v1 ────────────────────────────────────────
            yield {
                "event": "agent_start",
                "data": {
                    "agent": "Strategist",
                    "emoji": "🧠",
                    "message": f"The {captain_style} brain is formulating the tactical call...",
                    "turn": 2,
                    "total_turns": 5,
                },
            }

            propose, revise = create_strategist(client, model, captain_style)
            decision_v1_result = await propose(match_state, stats_result["report"])

            yield {
                "event": "agent_done",
                "data": {
                    "agent": "Strategist",
                    "emoji": "🧠",
                    "turn": 2,
                    "content": decision_v1_result["decision"],
                    "label": f"Decision v1 ({captain_style} Mode)",
                },
            }

            await asyncio.sleep(0.2)

            # ── TURN 3: Devil's Advocate ─────────────────────────────────────
            yield {
                "event": "agent_start",
                "data": {
                    "agent": "Devil's Advocate",
                    "emoji": "😈",
                    "message": "Challenging the call — finding every weakness in that strategy...",
                    "turn": 3,
                    "total_turns": 5,
                },
            }

            challenge = create_devils_advocate(client, model)
            objections_result = await challenge(
                match_state,
                decision_v1_result["decision"],
                stats_result["report"],
            )

            yield {
                "event": "agent_done",
                "data": {
                    "agent": "Devil's Advocate",
                    "emoji": "😈",
                    "turn": 3,
                    "content": objections_result["objections"],
                    "label": "Counter-Arguments",
                },
            }

            await asyncio.sleep(0.2)

            # ── TURN 4: Strategist v2 (revise or defend) ─────────────────────
            yield {
                "event": "agent_start",
                "data": {
                    "agent": "Strategist",
                    "emoji": "🧠",
                    "message": "Hearing the objections... refining or defending the call...",
                    "turn": 4,
                    "total_turns": 5,
                },
            }

            decision_v2_result = await revise(
                match_state,
                decision_v1_result["decision"],
                objections_result["objections"],
            )

            yield {
                "event": "agent_done",
                "data": {
                    "agent": "Strategist",
                    "emoji": "🧠",
                    "turn": 4,
                    "content": decision_v2_result["decision"],
                    "label": "Final Decision v2",
                },
            }

            await asyncio.sleep(0.2)

            # ── TURN 5: Commentator ──────────────────────────────────────────
            yield {
                "event": "agent_start",
                "data": {
                    "agent": "Commentator",
                    "emoji": "🎙️",
                    "message": "Translating the captain's call into cricket language for the fans...",
                    "turn": 5,
                    "total_turns": 5,
                },
            }

            narrate = create_commentator(client, model)
            commentary_result = await narrate(
                match_state,
                stats_result["report"],
                decision_v1_result["decision"],
                objections_result["objections"],
                decision_v2_result["decision"],
            )

            yield {
                "event": "agent_done",
                "data": {
                    "agent": "Commentator",
                    "emoji": "🎙️",
                    "turn": 5,
                    "content": commentary_result["commentary"],
                    "label": "Final Commentary",
                },
            }

            # ── COMPLETE ─────────────────────────────────────────────────────
            yield {
                "event": "complete",
                "data": {
                    "message": "Debate complete. Captain has spoken.",
                    "summary": {
                        "stats_report": stats_result["report"],
                        "decision_v1": decision_v1_result["decision"],
                        "objections": objections_result["objections"],
                        "decision_v2": decision_v2_result["decision"],
                        "commentary": commentary_result["commentary"],
                        "tool_calls_count": len(stats_result.get("tool_calls", [])),
                        "captain_style": captain_style,
                    },
                },
            }

        except Exception as e:
            yield {
                "event": "error",
                "data": {
                    "message": f"An error occurred during the debate: {str(e)}",
                    "error_type": type(e).__name__,
                },
            }

    return run_debate

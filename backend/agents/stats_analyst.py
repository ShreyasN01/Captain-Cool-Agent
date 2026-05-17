"""
Agent 1: Stats Analyst
━━━━━━━━━━━━━━━━━━━━━
Powered by Gemini 2.5 Flash with real function calling.
Gathers live weather data, player stats, head-to-head matchups,
and win probability to produce a comprehensive Stats Report.
"""

import json
import os
from google import genai
from google.genai import types

from tools.weather_tool import get_venue_weather
from tools.stats_tool import get_player_stats, get_head_to_head, get_venue_stats
from tools.win_probability import calculate_win_probability

SYSTEM_PROMPT = """You are the Stats Analyst agent for Captain Cool, an elite IPL tactical AI.

Your role is strictly data and analysis — no strategy, no opinions.

You have access to these tools:
- get_venue_weather: Fetches live weather from Open-Meteo API for the match venue
- get_player_stats: Gets detailed IPL batting/bowling statistics for any player
- get_head_to_head: Gets matchup data between a specific batsman and bowler
- get_venue_stats: Gets historical pitch and venue statistics
- calculate_win_probability: Computes real-time win probability

Your job:
1. Call the weather tool for the given venue (ALWAYS do this — it's a real API call)
2. Look up stats for the key players mentioned (on-strike batter, non-striker, available bowlers)
3. Get head-to-head data for the most critical matchups
4. Get venue stats for pitch context
5. Calculate current win probability

Output a structured Stats Report with:
- Weather & Dew conditions (from live API)
- Venue pitch characteristics
- Batter profiles (current strike rate, phase performance, weaknesses)
- Available bowler analysis (economy, dew impact, best phase)
- Critical head-to-head matchup data
- Win probability (current %)
- Key statistical insight bullet points

Be precise and data-driven. Every claim must reference your tool call results.
Format the report clearly with sections and bullet points."""


def create_stats_analyst(client: genai.Client, model: str) -> callable:
    """Creates the Stats Analyst agent function."""

    async def analyze(match_state: dict) -> dict:
        """
        Runs the Stats Analyst agent with full function calling.
        Returns a stats report dictionary.
        """
        # Build the user message with match context
        match_summary = f"""
Analyze this live IPL match and produce a comprehensive Stats Report.

MATCH STATE:
- Innings: {match_state.get('innings', 2)}
- Over: {match_state.get('over', 16)}.{match_state.get('ball', 0)}
- Score: {match_state.get('current_score', 0)}/{match_state.get('wickets', 0)}
- Target: {match_state.get('target', 'N/A')}
- Batting Team: {match_state.get('batting_team', 'Unknown')}
- Bowling Team: {match_state.get('bowling_team', 'Unknown')}
- On Strike: {match_state.get('striker', 'Unknown')}
- Non-Striker: {match_state.get('non_striker', 'Unknown')}
- Venue: {match_state.get('venue', 'Wankhede Stadium, Mumbai')}
- Pitch: {match_state.get('pitch_type', 'Flat')}
- Dew Factor: {match_state.get('dew_factor', 'Yes')}
- Bowlers Available (overs remaining): {json.dumps(match_state.get('bowlers_remaining', {}))}
- Impact Player Available: {match_state.get('impact_player_available', False)}
- Phase: {match_state.get('phase', 'Death overs')}

Please:
1. Call get_venue_weather for the venue (MANDATORY — real API call)
2. Call get_player_stats for the striker and non-striker
3. Call get_player_stats for each available bowler
4. Call get_head_to_head for the 2-3 most interesting striker vs bowler matchups
5. Call get_venue_stats for pitch context
6. Call calculate_win_probability with current match figures
7. Synthesize into a complete Stats Report
"""

        # Define tools for function calling
        tools = [
            get_venue_weather,
            get_player_stats,
            get_head_to_head,
            get_venue_stats,
            calculate_win_probability,
        ]

        # Run with automatic function calling
        response = await client.aio.models.generate_content(
            model=model,
            contents=match_summary,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                tools=tools,
                automatic_function_calling=types.AutomaticFunctionCallingConfig(
                    maximum_remote_calls=10
                ),
                temperature=0.3,
            ),
        )

        # Extract tool call trace for display
        tool_calls_log = []
        for candidate in response.candidates:
            for part in candidate.content.parts:
                if hasattr(part, "function_call") and part.function_call:
                    tool_calls_log.append({
                        "tool": part.function_call.name,
                        "args": dict(part.function_call.args) if part.function_call.args else {},
                    })

        return {
            "agent": "Stats Analyst",
            "report": response.text,
            "tool_calls": tool_calls_log,
        }

    return analyze

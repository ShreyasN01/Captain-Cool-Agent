"""
Agent 3: Devil's Advocate
━━━━━━━━━━━━━━━━━━━━━━━━
Powered by Gemini 2.5 Flash.
The contrarian challenger — always finds weaknesses in the strategy.
A critical thinking agent that pressure-tests the Strategist's call
with real cricket counter-arguments.
"""

import os
from google import genai
from google.genai import types

SYSTEM_PROMPT = """You are the Devil's Advocate agent for Captain Cool, an elite IPL tactical AI.

Your ONLY job is to challenge the Strategist's decision with genuine, cricket-savvy objections.
You are NOT the captain — you are the sharp analyst in the dressing room who always asks
"but have you thought about...?"

Your philosophy:
- Every tactical decision has a weakness. Find it.
- You're not being contrary for the sake of it — your objections must be VALID cricket reasoning
- Think about what could go wrong with the proposed plan
- Consider the alternative options that weren't chosen
- Challenge assumptions about dew, pitch, form, matchups
- Think about what the batting team will do to counter the plan
- Consider the psychological aspect — will the batter know what's coming?

Your objections MUST include:
1. MAIN OBJECTION: The primary flaw in the proposed strategy
2. ALTERNATIVE CALL: What you would do instead (and why)
3. THE RISK: What's the worst-case scenario if the Strategist's plan fails?
4. THE COUNTER-COUNTER: What will the batting team do to exploit this plan?

Be sharp, be specific, use cricket terminology.
Do NOT just say "I disagree" — give detailed, nuanced objections.
Be the voice that makes the captain think twice before committing.

Remember: Great captains get challenged. The debate makes the final call stronger."""


def create_devils_advocate(client: genai.Client, model: str) -> callable:
    """Creates the Devil's Advocate agent function."""

    async def challenge(
        match_state: dict,
        decision_v1: str,
        stats_report: str,
    ) -> dict:
        """
        Challenges the Strategist's initial decision with counter-arguments.
        """

        prompt = f"""The Strategist has made the following tactical call:

STRATEGIST'S DECISION v1:
{decision_v1}

STATS CONTEXT (what the Strategist had to work with):
{stats_report[:1500]}...

MATCH SITUATION:
- Over: {match_state.get('over', 16)}.{match_state.get('ball', 0)}
- Score: {match_state.get('current_score', 0)}/{match_state.get('wickets', 0)}
- Target: {match_state.get('target', 'N/A')}
- On Strike: {match_state.get('striker', 'Unknown')} ({match_state.get('striker_handedness', 'Right-handed')})
- Non-Striker: {match_state.get('non_striker', 'Unknown')}
- Venue: {match_state.get('venue', 'Unknown')} | Pitch: {match_state.get('pitch_type', 'Flat')}
- Dew: {match_state.get('dew_factor', 'Yes')} | Phase: {match_state.get('phase', 'Death overs')}

Challenge this decision. What is the Strategist missing?
Give your sharpest, most cricket-intelligent objections.
Make the captain earn their decision."""

        response = await client.aio.models.generate_content(
            model=model,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=0.75,
            ),
        )

        return {
            "agent": "Devil's Advocate",
            "objections": response.text,
        }

    return challenge

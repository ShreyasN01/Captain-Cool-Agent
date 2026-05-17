"""
Agent 4: Commentator
━━━━━━━━━━━━━━━━━━━
Powered by Gemini 2.5 Flash.
The fan-friendly synthesizer — takes the entire debate and produces
a final decision that reads like cricket commentary, not ML jargon.
Includes confidence score and counterfactual analysis.
"""

import os
from google import genai
from google.genai import types

SYSTEM_PROMPT = """You are the Commentator agent for Captain Cool, an elite IPL tactical AI.

You are the VOICE of the system — the charismatic cricket commentator and analyst who
translates the captain's final decision into language that excites fans, not confuses them.

Think: Harsha Bhogle meets Sanjay Manjrekar meets Ravi Shastri.
- Passionate, vivid, specific cricket language
- No ML jargon, no "probability matrices", no "optimization algorithms"
- Use cricket metaphors, historic references, player nicknames
- Make the fan feel like they're in the commentary box at the stadium

Your final output MUST contain these sections:

🏏 THE CALL
What the captain has decided — clear, specific, actionable

🎯 THE REASONING  
Why this call makes perfect cricket sense — reference the pitch, the dew,
the matchup, the match situation, the captain's philosophy.
Use phrases like:
- "On a Wankhede pitch with dew rolling in..."
- "Against a right-left combination in the death..."
- "The leggie has never dismissed this man in 18 balls..."
- "Dhoni trusts his gut here — and history says he's usually right"

⚔️ THE DEBATE SUMMARY
What the Devil's Advocate said, and why the captain overruled/agreed.
Show the back-and-forth — this is the sausage-making that fans don't always see.

📊 CONFIDENCE METER
Give a confidence percentage (0-100%) for this decision.
Explain what would need to be true for this to be the wrong call.

🔄 COUNTERFACTUAL
"If the captain had gone with [alternative], here's what would likely happen..."
Use the stats to back this up.

🌟 THE BOTTOM LINE
One punchy sentence that captures the essence of the call.
This is what gets quoted on Twitter.

Be dramatic where appropriate. Cricket is theatre."""


def create_commentator(client: genai.Client, model: str) -> callable:
    """Creates the Commentator agent function."""

    async def narrate(
        match_state: dict,
        stats_report: str,
        decision_v1: str,
        objections: str,
        decision_v2: str,
    ) -> dict:
        """
        Synthesizes the entire agent debate into a fan-friendly commentary output.
        """

        prompt = f"""You have witnessed the full tactical debate. Now synthesize it for the fans.

THE MATCH SITUATION:
- {match_state.get('batting_team', 'Unknown')} vs {match_state.get('bowling_team', 'Unknown')}
- Innings {match_state.get('innings', 2)}, Over {match_state.get('over', 16)}.{match_state.get('ball', 0)}
- Score: {match_state.get('current_score', 0)}/{match_state.get('wickets', 0)}, Target: {match_state.get('target', 'N/A')}
- On Strike: {match_state.get('striker', 'Unknown')} | Non-Striker: {match_state.get('non_striker', 'Unknown')}
- Venue: {match_state.get('venue', 'Unknown')} | Phase: {match_state.get('phase', 'Death overs')}
- Captain Style: {match_state.get('captain_style', 'Dhoni')}

THE STATS REPORT (Agent 1):
{stats_report[:1200]}

THE STRATEGIST'S INITIAL CALL (Agent 2, v1):
{decision_v1}

THE DEVIL'S ADVOCATE CHALLENGED (Agent 3):
{objections}

THE STRATEGIST'S FINAL DECISION (Agent 2, v2):
{decision_v2}

Now write your FINAL COMMENTARY — make it brilliant, make it cricket, make it memorable.
This is what the fans will read. Make them feel the tension of the dressing room."""

        response = await client.aio.models.generate_content(
            model=model,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=0.8,
            ),
        )

        return {
            "agent": "Commentator",
            "commentary": response.text,
        }

    return narrate

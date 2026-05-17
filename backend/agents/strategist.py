"""
Agent 2: Strategist
━━━━━━━━━━━━━━━━━━
Powered by Gemini 2.5 Flash.
The primary captain brain — proposes tactical decisions based on
stats, match context, and the selected captain's playing style.
Runs twice: initial proposal (v1) and revised/defended response (v2).
"""

import os
from google import genai
from google.genai import types

SYSTEM_PROMPT_TEMPLATE = """You are the Strategist agent for Captain Cool, an elite IPL tactical AI.

You are channelling the playing style and philosophy of: {captain_style}

{captain_description}

Your role is to make THE tactical decision for the next action in this match.
You have been given a Stats Report from the Stats Analyst. Use it as your foundation.

When making your decision, think like a real IPL captain:
- Field placements and how they set up the over
- Match situation vs bowler's strengths and weaknesses
- The batter's known weaknesses and how to exploit them
- Dew conditions and how they affect spin vs pace
- Wickets in hand, run rate pressure, required rate
- Over-by-over planning (who bowls which over)
- Impact Player strategy
- Powerplay vs middle overs vs death overs tactics
- Left-right combination disruption

Your decision must cover:
1. PRIMARY DECISION: Who bowls the next over / who comes in / field change / timeout
2. OVER PLAN: Brief plan for overs 17-20 (if death overs)
3. FIELD SETUP: Key fielders placed for this over
4. WHY THIS BOWLER/BATTER: Cricket-language reasoning
5. WHAT I'M TRYING TO ACHIEVE: Wicket? Dot balls? Contain to X runs?

Be decisive. A captain doesn't hedge — they commit to a plan.
Speak like a seasoned IPL captain or analyst, not a robot.
Use cricket terms naturally."""

CAPTAIN_STYLES = {
    "Dhoni": {
        "description": """Captain: MS Dhoni — The Finisher, The Strategist, Captain Cool himself.

Philosophy: "Trust the process. Trust your bowlers. Don't panic."
- Always calm, calculating, and two steps ahead
- Renowned for backing his bowlers even under pressure
- Masters the death-over field placements — unconventional but highly effective
- Believes in finishing with a flourish — set up the equation for the last 2 overs
- "Thala knows what he's doing" — always has a plan within a plan
- Loves the strategic timeout to reset after a big over
- Never shows emotion — decisions are clinical, data-driven, match-situation dependent
- Famous for keeping 7 or 8 on the on-side in death overs
- Always backs the big-match player in crunch moments""",
    },
    "Rohit": {
        "description": """Captain: Rohit Sharma — The Hitman Captain, Aggressive & Instinctive.

Philosophy: "Attack is the best defence. Set the game up early."
- Believes in taking the game on from ball one
- Famous for back-to-back 5 IPL titles with Mumbai Indians
- Very aggressive bowling changes — bowlers rotate rapidly to keep batters guessing
- Will gamble with a spinner in the powerplay if there's turn
- Trusts his pace trio (Bumrah/Boult) to win him games
- "Never let the opposition settle"
- Backs his big hitters to do the job in the last 3 overs
- Very data-aware, works closely with analytics team
- Will bring back his best bowler even if expensive earlier""",
    },
    "Hardik": {
        "description": """Captain: Hardik Pandya — The Maverick, Bold & Instinctive.

Philosophy: "Believe in yourself. Attack every situation. Express your game."
- Unconventional, instinct-driven decisions that keep opponents guessing
- Believes in himself as a match-winner — leads from the front
- Very aggressive — will change bowler mid-plan if it's not working
- Loves setting attacking fields early and trusting bowlers to back it
- Will use himself at critical moments — believes all-rounders change games
- "Fortune favours the bold"
- Less conservative than Dhoni, more willing to take risks
- Strong belief in youngsters and will back them in pressure moments""",
    },
}


def create_strategist(client: genai.Client, model: str, captain_style: str = "Dhoni") -> callable:
    """Creates the Strategist agent with the given captain style."""

    style_info = CAPTAIN_STYLES.get(captain_style, CAPTAIN_STYLES["Dhoni"])
    system_prompt = SYSTEM_PROMPT_TEMPLATE.format(
        captain_style=captain_style,
        captain_description=style_info["description"],
    )

    async def propose(match_state: dict, stats_report: str) -> dict:
        """Initial strategic proposal based on stats report."""

        prompt = f"""You have the following Stats Report from your analyst:

{stats_report}

CURRENT MATCH STATE:
- Over: {match_state.get('over', 16)}.{match_state.get('ball', 0)}
- Score: {match_state.get('current_score', 0)}/{match_state.get('wickets', 0)}
- Target: {match_state.get('target', 'N/A')} | Phase: {match_state.get('phase', 'Death overs')}
- On Strike: {match_state.get('striker', 'Unknown')} | Non-Striker: {match_state.get('non_striker', 'Unknown')}
- Bowlers & Overs Used: {match_state.get('bowlers_used', {})}
- Bowlers Remaining (overs left): {match_state.get('bowlers_remaining', {})}
- Impact Player Available: {match_state.get('impact_player_available', False)}
- Venue: {match_state.get('venue', 'Unknown')} | Pitch: {match_state.get('pitch_type', 'Flat')}

Now make your tactical call. This is YOUR DECISION v1 — be decisive and specific.
What happens NEXT over? Set the field. Name your bowler. Tell me the plan."""

        response = await client.aio.models.generate_content(
            model=model,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=0.7,
            ),
        )

        return {
            "agent": "Strategist",
            "version": "v1",
            "captain_style": captain_style,
            "decision": response.text,
        }

    async def revise(match_state: dict, decision_v1: str, objections: str) -> dict:
        """Revised decision after hearing Devil's Advocate objections."""

        prompt = f"""You made your initial tactical call:

YOUR DECISION v1:
{decision_v1}

Now your Devil's Advocate has challenged you:

DEVIL'S ADVOCATE OBJECTIONS:
{objections}

As captain, you must either:
A) DEFEND your original call with additional reasoning, OR
B) REVISE your decision if the objection reveals a genuine flaw

Be honest. If they made a good point, say so and adjust.
If you're sticking to your guns, explain WHY their objection doesn't hold up in this situation.

Output your FINAL DECISION v2 — this is what you're going with. Own it.

Current match state for reference:
- Over: {match_state.get('over', 16)}.{match_state.get('ball', 0)} | Score: {match_state.get('current_score', 0)}/{match_state.get('wickets', 0)}
- Phase: {match_state.get('phase', 'Death overs')} | Venue: {match_state.get('venue', 'Unknown')}"""

        response = await client.aio.models.generate_content(
            model=model,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=0.65,
            ),
        )

        return {
            "agent": "Strategist",
            "version": "v2",
            "captain_style": captain_style,
            "decision": response.text,
        }

    return propose, revise

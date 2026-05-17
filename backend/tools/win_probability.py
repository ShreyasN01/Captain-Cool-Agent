"""
Win Probability Calculator
Computes real-time win probability for the batting team using a
run-rate based model with wicket-in-hand adjustments.
"""

import math


def calculate_win_probability(
    innings: int,
    current_score: int,
    wickets_fallen: int,
    balls_bowled: int,
    target: int | None = None,
    total_overs: int = 20,
) -> dict:
    """
    Calculate win probability for the batting team.

    Args:
        innings: 1 or 2
        current_score: Runs scored so far
        wickets_fallen: Wickets lost
        balls_bowled: Balls bowled so far (e.g. 18.3 overs = 18*6+3 = 111)
        target: Required target (only for 2nd innings)
        total_overs: Total overs in the match (default 20)

    Returns:
        Dictionary with win_probability (0-100), required_run_rate,
        current_run_rate, balls_remaining, and a narrative summary.
    """
    total_balls = total_overs * 6
    balls_remaining = total_balls - balls_bowled
    wickets_remaining = 10 - wickets_fallen
    current_rr = (current_score / balls_bowled * 6) if balls_bowled > 0 else 0

    if innings == 1:
        # First innings: project final score and probability of posting 160+
        projected_score = current_score + (current_rr * balls_remaining / 6)
        # Penalise for wickets lost
        wicket_factor = 0.9 ** (wickets_fallen)
        projected_score *= wicket_factor
        win_prob = min(95, max(5, 50 + (projected_score - 165) * 0.8))
        rrr = None
        summary = (
            f"Projected score: ~{projected_score:.0f}. "
            f"Batting team win probability: {win_prob:.1f}%"
        )
    else:
        # Second innings: need runs with wickets in hand
        if target is None:
            target = 180  # default
        runs_needed = target - current_score
        if runs_needed <= 0:
            return {
                "win_probability": 100,
                "required_run_rate": 0,
                "current_run_rate": round(current_rr, 2),
                "balls_remaining": balls_remaining,
                "runs_needed": 0,
                "summary": "Target already achieved! Batting team wins!",
            }
        if balls_remaining <= 0:
            return {
                "win_probability": 0,
                "required_run_rate": 999,
                "current_run_rate": round(current_rr, 2),
                "balls_remaining": 0,
                "runs_needed": runs_needed,
                "summary": "Match over — batting team failed to chase.",
            }

        rrr = runs_needed / balls_remaining * 6

        # Sigmoid-based model: centred on RRR vs current RR
        rr_diff = current_rr - rrr  # positive = on track
        # Wicket factor: fewer wickets = harder to win
        wicket_factor = math.log(wickets_remaining + 1) / math.log(11)
        # Base probability from run rate differential
        base = 1 / (1 + math.exp(-0.4 * rr_diff))
        win_prob = base * wicket_factor * 100
        win_prob = min(97, max(3, win_prob))

        summary = (
            f"Need {runs_needed} off {balls_remaining} balls (RRR: {rrr:.2f}). "
            f"Current RR: {current_rr:.2f}. Wickets in hand: {wickets_remaining}. "
            f"Win probability: {win_prob:.1f}%"
        )

    return {
        "win_probability": round(win_prob, 1),
        "required_run_rate": round(rrr, 2) if rrr is not None else None,
        "current_run_rate": round(current_rr, 2),
        "balls_remaining": balls_remaining,
        "runs_needed": runs_needed if innings == 2 else None,
        "summary": summary,
    }

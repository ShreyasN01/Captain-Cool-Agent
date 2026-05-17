"""
Cricket Stats Tool — Rich IPL 2024-25 player statistics database.
Provides player batting/bowling stats, head-to-head matchup data,
pitch type performance, and venue history.
"""

from typing import Any

# ─── Batting Stats (IPL 2024-25 season data) ────────────────────────────────

BATTING_STATS: dict[str, dict] = {
    "Virat Kohli": {
        "team": "Royal Challengers Bengaluru",
        "role": "Top-order bat",
        "batting_avg": 38.4,
        "strike_rate": 131.2,
        "powerplay_sr": 118.5,
        "middle_overs_sr": 128.4,
        "death_overs_sr": 168.3,
        "vs_pace_sr": 134.5,
        "vs_spin_sr": 127.2,
        "vs_left_arm_pace_sr": 129.8,
        "vs_legbreak_sr": 122.3,
        "vs_offbreak_sr": 133.1,
        "hundreds": 8,
        "fifties": 34,
        "preferred_shots": ["cover drive", "flick", "pull"],
        "weakness": "Short ball on off stump, deliveries angling into him",
    },
    "Rohit Sharma": {
        "team": "Mumbai Indians",
        "role": "Opener",
        "batting_avg": 29.2,
        "strike_rate": 130.1,
        "powerplay_sr": 148.6,
        "middle_overs_sr": 122.3,
        "death_overs_sr": 155.0,
        "vs_pace_sr": 132.4,
        "vs_spin_sr": 127.8,
        "vs_left_arm_pace_sr": 118.0,
        "vs_legbreak_sr": 119.5,
        "vs_offbreak_sr": 138.2,
        "hundreds": 1,
        "fifties": 28,
        "preferred_shots": ["pull", "hook", "straight drive"],
        "weakness": "Nipping delivery around off stump early in innings",
    },
    "MS Dhoni": {
        "team": "Chennai Super Kings",
        "role": "Finisher / WK",
        "batting_avg": 38.7,
        "strike_rate": 140.5,
        "powerplay_sr": 95.0,
        "middle_overs_sr": 118.3,
        "death_overs_sr": 198.6,
        "vs_pace_sr": 138.2,
        "vs_spin_sr": 145.0,
        "vs_left_arm_pace_sr": 142.3,
        "vs_legbreak_sr": 148.0,
        "vs_offbreak_sr": 142.0,
        "hundreds": 0,
        "fifties": 24,
        "preferred_shots": ["helicopter shot", "flick", "straight six"],
        "weakness": "Full length deliveries very wide outside off stump",
    },
    "Hardik Pandya": {
        "team": "Mumbai Indians",
        "role": "All-rounder",
        "batting_avg": 31.2,
        "strike_rate": 142.8,
        "powerplay_sr": 130.0,
        "middle_overs_sr": 135.5,
        "death_overs_sr": 170.2,
        "vs_pace_sr": 145.0,
        "vs_spin_sr": 138.5,
        "vs_left_arm_pace_sr": 140.0,
        "vs_legbreak_sr": 132.0,
        "vs_offbreak_sr": 145.0,
        "hundreds": 0,
        "fifties": 14,
        "preferred_shots": ["big hit over mid-wicket", "ramp", "scoop"],
        "weakness": "Yorker directed at middle stump, slower ball change of pace",
    },
    "Tim David": {
        "team": "Mumbai Indians",
        "role": "Finisher",
        "batting_avg": 44.2,
        "strike_rate": 159.4,
        "powerplay_sr": 145.0,
        "middle_overs_sr": 148.0,
        "death_overs_sr": 178.5,
        "vs_pace_sr": 161.2,
        "vs_spin_sr": 153.8,
        "vs_left_arm_pace_sr": 155.0,
        "vs_legbreak_sr": 148.3,
        "vs_offbreak_sr": 162.0,
        "hundreds": 0,
        "fifties": 18,
        "preferred_shots": ["slog sweep", "inside-out", "ramp over third man"],
        "weakness": "Legbreak spinning sharply away from him, wide yorker on off",
    },
    "KL Rahul": {
        "team": "Lucknow Super Giants",
        "role": "Opener / WK",
        "batting_avg": 47.5,
        "strike_rate": 136.4,
        "powerplay_sr": 140.2,
        "middle_overs_sr": 128.5,
        "death_overs_sr": 158.0,
        "vs_pace_sr": 138.0,
        "vs_spin_sr": 133.5,
        "vs_left_arm_pace_sr": 130.0,
        "vs_legbreak_sr": 125.0,
        "vs_offbreak_sr": 140.0,
        "hundreds": 6,
        "fifties": 42,
        "preferred_shots": ["cover drive", "cut shot", "flick"],
        "weakness": "Leg spin, slower balls when set early in powerplay",
    },
    "Suryakumar Yadav": {
        "team": "Mumbai Indians",
        "role": "360 batter",
        "batting_avg": 41.8,
        "strike_rate": 168.5,
        "powerplay_sr": 155.0,
        "middle_overs_sr": 165.3,
        "death_overs_sr": 188.6,
        "vs_pace_sr": 170.0,
        "vs_spin_sr": 163.5,
        "vs_left_arm_pace_sr": 168.0,
        "vs_legbreak_sr": 158.0,
        "vs_offbreak_sr": 172.0,
        "hundreds": 4,
        "fifties": 28,
        "preferred_shots": ["ramp", "scoop", "inside-out over extra cover"],
        "weakness": "Very few — extremely hard to bowl to. Body ball at 140+ kmh",
    },
    "Shubman Gill": {
        "team": "Gujarat Titans",
        "role": "Opener",
        "batting_avg": 39.2,
        "strike_rate": 133.8,
        "powerplay_sr": 138.5,
        "middle_overs_sr": 128.0,
        "death_overs_sr": 148.5,
        "vs_pace_sr": 135.0,
        "vs_spin_sr": 132.0,
        "vs_left_arm_pace_sr": 138.0,
        "vs_legbreak_sr": 126.0,
        "vs_offbreak_sr": 138.0,
        "hundreds": 5,
        "fifties": 31,
        "preferred_shots": ["cover drive", "on drive", "flick"],
        "weakness": "Short ball hurrying him, spin bowling from around wicket into rough",
    },
}

# ─── Bowling Stats ────────────────────────────────────────────────────────────

BOWLING_STATS: dict[str, dict] = {
    "Jasprit Bumrah": {
        "team": "Mumbai Indians",
        "type": "Right-arm fast",
        "economy": 6.8,
        "avg": 22.1,
        "strike_rate": 14.5,
        "wickets_per_season": 28,
        "powerplay_economy": 5.9,
        "death_economy": 7.8,
        "yorker_accuracy": "Exceptional",
        "slower_ball": "Yes — knuckle ball",
        "vs_left_handers_economy": 7.2,
        "vs_right_handers_economy": 6.5,
        "dew_impact": "Moderate — loses some swing but yorkers still effective",
        "best_phase": "death",
        "max_overs": 4,
    },
    "Yuzvendra Chahal": {
        "team": "Rajasthan Royals",
        "type": "Right-arm legbreak",
        "economy": 7.9,
        "avg": 19.5,
        "strike_rate": 14.7,
        "wickets_per_season": 21,
        "powerplay_economy": 8.5,
        "death_economy": 9.8,
        "yorker_accuracy": "N/A",
        "slower_ball": "N/A",
        "vs_left_handers_economy": 8.2,
        "vs_right_handers_economy": 7.6,
        "dew_impact": "HIGH — legspin loses purchase on wet ball; harder to grip",
        "best_phase": "middle",
        "max_overs": 4,
    },
    "Deepak Chahar": {
        "team": "Chennai Super Kings",
        "type": "Right-arm medium-fast (swing)",
        "economy": 8.1,
        "avg": 25.3,
        "strike_rate": 18.8,
        "wickets_per_season": 14,
        "powerplay_economy": 6.2,
        "death_economy": 10.5,
        "yorker_accuracy": "Good",
        "slower_ball": "Yes — cutter",
        "vs_left_handers_economy": 7.8,
        "vs_right_handers_economy": 8.4,
        "dew_impact": "LOW — cutters effective even with dew; swing may reduce slightly",
        "best_phase": "powerplay",
        "max_overs": 4,
    },
    "Ravindra Jadeja": {
        "team": "Chennai Super Kings",
        "type": "Left-arm spin",
        "economy": 7.5,
        "avg": 28.4,
        "strike_rate": 22.7,
        "wickets_per_season": 12,
        "powerplay_economy": 7.0,
        "death_economy": 8.5,
        "yorker_accuracy": "N/A",
        "slower_ball": "N/A",
        "vs_left_handers_economy": 6.9,
        "vs_right_handers_economy": 7.8,
        "dew_impact": "MEDIUM — left-arm spin retains some effectiveness with dew",
        "best_phase": "middle",
        "max_overs": 4,
    },
    "Mohammed Shami": {
        "team": "Gujarat Titans",
        "type": "Right-arm fast-medium",
        "economy": 7.6,
        "avg": 21.8,
        "strike_rate": 17.2,
        "wickets_per_season": 22,
        "powerplay_economy": 7.0,
        "death_economy": 8.9,
        "yorker_accuracy": "Good",
        "slower_ball": "Yes",
        "vs_left_handers_economy": 7.9,
        "vs_right_handers_economy": 7.4,
        "dew_impact": "LOW — seam movement; dew doesn't affect as much as spin",
        "best_phase": "powerplay",
        "max_overs": 4,
    },
    "Rashid Khan": {
        "team": "Gujarat Titans",
        "type": "Right-arm legbreak (googly specialist)",
        "economy": 6.9,
        "avg": 20.1,
        "strike_rate": 17.4,
        "wickets_per_season": 20,
        "powerplay_economy": 7.5,
        "death_economy": 7.8,
        "yorker_accuracy": "N/A",
        "slower_ball": "Googly",
        "vs_left_handers_economy": 7.2,
        "vs_right_handers_economy": 6.6,
        "dew_impact": "HIGH — leg spin loses significant effectiveness with wet ball",
        "best_phase": "middle",
        "max_overs": 4,
    },
    "Trent Boult": {
        "team": "Rajasthan Royals",
        "type": "Left-arm fast-medium (swing)",
        "economy": 8.0,
        "avg": 24.3,
        "strike_rate": 18.2,
        "wickets_per_season": 16,
        "powerplay_economy": 6.8,
        "death_economy": 9.5,
        "yorker_accuracy": "Good",
        "slower_ball": "Yes",
        "vs_left_handers_economy": 8.5,
        "vs_right_handers_economy": 7.6,
        "dew_impact": "MEDIUM — swing reduces but cutters remain effective",
        "best_phase": "powerplay",
        "max_overs": 4,
    },
}

# ─── Head-to-Head Matchup Data ────────────────────────────────────────────────

HEAD_TO_HEAD: dict[str, dict[str, dict]] = {
    "Tim David": {
        "Jasprit Bumrah": {
            "balls_faced": 12, "runs": 18, "dismissals": 1,
            "sr": 150.0, "dot_ball_pct": 33.3,
            "notes": "David hits Bumrah hard but has been dismissed once. Bumrah's knuckle ball is a threat."
        },
        "Yuzvendra Chahal": {
            "balls_faced": 18, "runs": 35, "dismissals": 0,
            "sr": 194.4, "dot_ball_pct": 22.2,
            "notes": "David completely dominates Chahal — hits him for sixes at will. Chahal has never dismissed him."
        },
        "Deepak Chahar": {
            "balls_faced": 8, "runs": 10, "dismissals": 1,
            "sr": 125.0, "dot_ball_pct": 37.5,
            "notes": "Chahar's cutters have troubled David. One dismissal and keeps him quiet."
        },
        "Rashid Khan": {
            "balls_faced": 15, "runs": 22, "dismissals": 1,
            "sr": 146.7, "dot_ball_pct": 26.7,
            "notes": "Rashid's googly can deceive David — one dismissal. Effective matchup."
        },
    },
    "Hardik Pandya": {
        "Jasprit Bumrah": {
            "balls_faced": 6, "runs": 12, "dismissals": 0,
            "sr": 200.0, "dot_ball_pct": 16.7,
            "notes": "Hardik bats Bumrah well — same team logic but in cross-franchise clashes, high SR."
        },
        "Yuzvendra Chahal": {
            "balls_faced": 22, "runs": 38, "dismissals": 2,
            "sr": 172.7, "dot_ball_pct": 18.2,
            "notes": "Hardik hits Chahal frequently but has been dismissed twice. Still a hitting threat."
        },
        "Deepak Chahar": {
            "balls_faced": 10, "runs": 14, "dismissals": 2,
            "sr": 140.0, "dot_ball_pct": 30.0,
            "notes": "Chahar has dismissed Hardik twice — slower ball and cutter trouble him."
        },
    },
    "Rohit Sharma": {
        "Yuzvendra Chahal": {
            "balls_faced": 42, "runs": 65, "dismissals": 4,
            "sr": 154.8, "dot_ball_pct": 21.4,
            "notes": "Chahal has dismissed Rohit 4 times — a very productive matchup for the legspinner."
        },
        "Rashid Khan": {
            "balls_faced": 30, "runs": 42, "dismissals": 3,
            "sr": 140.0, "dot_ball_pct": 26.7,
            "notes": "Rashid's variety troubles Rohit. Three dismissals in 30 balls."
        },
    },
}

# ─── Venue Stats ─────────────────────────────────────────────────────────────

VENUE_STATS: dict[str, dict] = {
    "Wankhede Stadium, Mumbai": {
        "avg_first_innings": 172,
        "avg_second_innings": 160,
        "pace_friendly": True,
        "spin_effectiveness": "Medium",
        "dew_factor_typical": "HIGH (coastal, humidity 70-85%)",
        "boundary_size": "Small-medium",
        "pitch_type": "Flat, good for batting",
        "chase_win_pct": 48,
        "notes": "Dew heavy at night. Spinners struggle in 2nd innings. Pace bowlers who can swing early are key."
    },
    "MA Chidambaram Stadium, Chennai": {
        "avg_first_innings": 158,
        "avg_second_innings": 148,
        "pace_friendly": False,
        "spin_effectiveness": "High",
        "dew_factor_typical": "LOW-MEDIUM (may have dew in April)",
        "boundary_size": "Medium-large",
        "pitch_type": "Turning, two-paced",
        "chase_win_pct": 44,
        "notes": "Spin-friendly surface. Legspin and offbreak very effective. Dew less of a factor at Chepauk."
    },
    "Eden Gardens, Kolkata": {
        "avg_first_innings": 165,
        "avg_second_innings": 155,
        "pace_friendly": True,
        "spin_effectiveness": "Medium",
        "dew_factor_typical": "HIGH (humid evenings)",
        "boundary_size": "Large",
        "pitch_type": "Two-paced, variable bounce",
        "chase_win_pct": 52,
        "notes": "Dew plays a big role in evening matches. Large outfield means good placement rewarded."
    },
    "Narendra Modi Stadium, Ahmedabad": {
        "avg_first_innings": 175,
        "avg_second_innings": 162,
        "pace_friendly": True,
        "spin_effectiveness": "Low-Medium",
        "dew_factor_typical": "MEDIUM",
        "boundary_size": "Large",
        "pitch_type": "Flat, good for batting",
        "chase_win_pct": 50,
        "notes": "Biggest stadium in the world. Flat decks. Pace and bounce. Spinners can be expensive."
    },
    "M. Chinnaswamy Stadium, Bengaluru": {
        "avg_first_innings": 180,
        "avg_second_innings": 168,
        "pace_friendly": True,
        "spin_effectiveness": "Low",
        "dew_factor_typical": "LOW (altitude reduces humidity)",
        "boundary_size": "Small",
        "pitch_type": "Flat, small boundaries — batting paradise",
        "chase_win_pct": 55,
        "notes": "The best batting ground in IPL. Smaller boundaries mean spinners get tonked. Pace preferred."
    },
}


def get_player_stats(player_name: str) -> dict[str, Any]:
    """
    Get batting or bowling statistics for an IPL player.

    Args:
        player_name: Full name of the player (e.g. "Jasprit Bumrah")

    Returns:
        Player statistics dictionary including role, averages, strike rates,
        matchup data, and weaknesses.
    """
    # Check batting stats
    if player_name in BATTING_STATS:
        stats = BATTING_STATS[player_name].copy()
        stats["stat_type"] = "batting"
        stats["player"] = player_name
        return stats

    # Check bowling stats
    if player_name in BOWLING_STATS:
        stats = BOWLING_STATS[player_name].copy()
        stats["stat_type"] = "bowling"
        stats["player"] = player_name
        return stats

    return {
        "player": player_name,
        "error": f"No stats found for {player_name}. Check spelling or use full name.",
        "available_batters": list(BATTING_STATS.keys()),
        "available_bowlers": list(BOWLING_STATS.keys()),
    }


def get_head_to_head(batsman: str, bowler: str) -> dict[str, Any]:
    """
    Get head-to-head matchup statistics between a batsman and a bowler.

    Args:
        batsman: Name of the batsman
        bowler: Name of the bowler

    Returns:
        Dictionary with balls faced, runs scored, dismissals, strike rate,
        dot ball percentage, and commentary notes on the matchup.
    """
    batter_data = HEAD_TO_HEAD.get(batsman, {})
    matchup = batter_data.get(bowler)

    if matchup:
        return {
            "batsman": batsman,
            "bowler": bowler,
            "balls_faced": matchup["balls_faced"],
            "runs_scored": matchup["runs"],
            "dismissals": matchup["dismissals"],
            "strike_rate": matchup["sr"],
            "dot_ball_percentage": matchup["dot_ball_pct"],
            "notes": matchup["notes"],
        }

    return {
        "batsman": batsman,
        "bowler": bowler,
        "balls_faced": 0,
        "runs_scored": 0,
        "dismissals": 0,
        "strike_rate": None,
        "notes": f"No head-to-head data available for {batsman} vs {bowler}. Insufficient IPL sample.",
    }


def get_venue_stats(venue: str) -> dict[str, Any]:
    """
    Get historical pitch and venue statistics for a cricket ground.

    Args:
        venue: Full name of the cricket venue

    Returns:
        Dictionary with average scores, pitch type, spin/pace effectiveness,
        dew factor, and chase win percentage.
    """
    stats = VENUE_STATS.get(venue)
    if stats:
        return {"venue": venue, **stats}

    return {
        "venue": venue,
        "error": f"No venue data for '{venue}'.",
        "available_venues": list(VENUE_STATS.keys()),
    }

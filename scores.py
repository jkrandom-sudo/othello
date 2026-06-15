"""
Score tracking and leaderboard module.
Persists scores to scores.json.
"""

from __future__ import annotations

import json
import os
from datetime import datetime
from typing import Any, Dict, List, Optional

SCORES_FILE = "scores.json"


def load_scores() -> List[Dict[str, Any]]:
    """Load all scores from scores.json."""
    if os.path.exists(SCORES_FILE):
        try:
            with open(SCORES_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
        except (json.JSONDecodeError, IOError):
            pass
    return []


def save_scores(scores: List[Dict[str, Any]]) -> None:
    """Save scores list to scores.json."""
    with open(SCORES_FILE, "w", encoding="utf-8") as f:
        json.dump(scores, f, ensure_ascii=False, indent=2)


def add_score(
    player_name: str,
    score: int,
    difficulty: str,
    winner: str,
) -> None:
    """Add a new score record."""
    scores = load_scores()
    scores.append({
        "player_name": player_name,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "score": score,
        "difficulty": difficulty,
        "winner": winner,
    })
    save_scores(scores)


def get_top_scores(n: int = 10) -> List[Dict[str, Any]]:
    """Return the top N scores sorted by score descending."""
    scores = load_scores()
    scores_sorted = sorted(scores, key=lambda s: s.get("score", 0), reverse=True)
    return scores_sorted[:n]

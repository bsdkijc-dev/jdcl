"""Leaderboard data model (strictly empty until real verified submissions)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class LeaderboardEntry:
    participant_id: str
    submission_id: str
    mae: float
    rmse: float
    r2: float
    reproducible: bool
    submitted_utc: str
    is_baseline: bool = False


@dataclass
class Leaderboard:
    competition_id: str
    entries: List[LeaderboardEntry] = field(default_factory=list)

    def add_entry(self, entry: LeaderboardEntry) -> None:
        self.entries.append(entry)
        self.entries.sort(key=lambda e: (e.mae, e.rmse))

    def to_list(self) -> List[Dict[str, Any]]:
        return [
            {
                "rank": i + 1,
                "participant_id": e.participant_id,
                "submission_id": e.submission_id,
                "mae": e.mae,
                "rmse": e.rmse,
                "r2": e.r2,
                "reproducible": e.reproducible,
                "submitted_utc": e.submitted_utc,
                "is_baseline": e.is_baseline,
            }
            for i, e in enumerate(self.entries)
        ]

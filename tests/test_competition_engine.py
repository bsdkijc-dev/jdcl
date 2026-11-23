"""Tests for competition engine, scoring, reproducibility, and empty leaderboard."""

import unittest

import pandas as pd

from jdcl.competition.engine import CompetitionEngine
from jdcl.data.generator import generate_jflm_2027_dataframe
from jdcl.models.baselines import deterministic_split


class TestCompetitionEngine(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = CompetitionEngine("jflm-2027")
        df = generate_jflm_2027_dataframe(n_rows=400, seed=20270101)
        self.test_df = deterministic_split(df, seed=20270101).test_df

    def test_leaderboard_starts_empty_no_fake_entries(self) -> None:
        self.assertEqual(len(self.engine.leaderboard.entries), 0)

    def test_valid_submission_scoring_and_reproducibility(self) -> None:
        sub = pd.DataFrame({
            "record_id": self.test_df["record_id"],
            "predicted_resolution_days": self.test_df["resolution_days"],
        })
        res = self.engine.evaluate_submission(self.test_df, sub, sub)
        self.assertTrue(res["valid"])
        self.assertTrue(res["reproducible"])
        self.assertEqual(res["metrics"]["mae"], 0.0)
        self.assertEqual(res["metrics"]["rmse"], 0.0)

    def test_invalid_submission_bounds_rejected(self) -> None:
        sub = pd.DataFrame({
            "record_id": self.test_df["record_id"],
            "predicted_resolution_days": -10.0,
        })
        res = self.engine.evaluate_submission(self.test_df, sub)
        self.assertFalse(res["valid"])


if __name__ == "__main__":
    unittest.main()

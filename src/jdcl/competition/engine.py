"""Competition Engine orchestrating evaluation, reproducibility, and reporting."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

import numpy as np
import pandas as pd

from jdcl.competition.leaderboard import Leaderboard
from jdcl.competition.registry import get_competition_metadata
from jdcl.competition.scoring import score_submission, validate_submission
from jdcl.config import PROJECT_ROOT, load_yaml
from jdcl.models.fairness import compute_subgroup_fairness


class CompetitionEngine:
    def __init__(self, competition_id: str = "jflm-2027") -> None:
        self.competition_id = competition_id
        self.metadata = get_competition_metadata(competition_id)
        self.hidden_eval = load_yaml(PROJECT_ROOT / "config" / "hidden_eval_config.yml")
        self.submission_schema = load_yaml(PROJECT_ROOT / self.metadata["submission_schema_path"])
        # Strictly empty by default: no fake participants or fake scores
        self.leaderboard = Leaderboard(competition_id=competition_id)

    def get_rules_and_eligibility(self) -> Dict[str, Any]:
        return {
            "competition_id": self.competition_id,
            "platform": self.metadata["platform"],
            "cost_tier": self.metadata["cost_tier"],
            "status": self.metadata["status"],
            "prizes": self.metadata["prizes"],
            "prohibited_actions": self.metadata["prohibited_actions"],
            "human_approval_required": self.metadata["human_approval_required"],
        }

    def evaluate_submission(
        self,
        ground_truth_df: pd.DataFrame,
        submission_df: pd.DataFrame,
        repeat_submission_df: pd.DataFrame | None = None,
    ) -> Dict[str, Any]:
        id_col = self.hidden_eval.get("id_column", "record_id")
        target_col = self.hidden_eval.get("target_column", "resolution_days")
        errors = validate_submission(submission_df, ground_truth_df[id_col], self.submission_schema)
        if errors:
            return {"valid": False, "errors": errors}

        metrics = score_submission(ground_truth_df, submission_df, id_col=id_col, target_col=target_col)

        reproducible = True
        if repeat_submission_df is not None:
            tol = float(self.hidden_eval.get("reproducibility", {}).get("max_score_tolerance", 1e-6))
            m2 = score_submission(ground_truth_df, repeat_submission_df, id_col=id_col, target_col=target_col)
            reproducible = abs(metrics["mae"] - m2["mae"]) <= tol and abs(metrics["rmse"] - m2["rmse"]) <= tol

        merged = ground_truth_df.merge(
            submission_df[[id_col, "predicted_resolution_days"]],
            on=id_col,
            how="inner",
        )
        fairness = {}
        for grp_col in self.hidden_eval.get("protected_group_columns", []):
            fairness[grp_col] = compute_subgroup_fairness(
                merged, target_col, merged["predicted_resolution_days"].to_numpy(dtype=float), grp_col
            )

        return {
            "valid": True,
            "competition_id": self.competition_id,
            "evaluated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "metrics": metrics,
            "reproducible": reproducible,
            "fairness": fairness,
        }

    def generate_result_report(self, eval_result: Dict[str, Any], output_path: Path) -> Path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        lines = [
            f"# Competition Evaluation Report — {self.competition_id}",
            "",
            f"- **Evaluated UTC:** {eval_result.get('evaluated_utc', 'N/A')}",
            f"- **Valid Submission:** {eval_result.get('valid', False)}",
            f"- **Reproducible:** {eval_result.get('reproducible', False)}",
            "",
            "> **Synthetic Disclaimer:** Evaluation conducted on 100% synthetic holdout data.",
            "",
        ]
        if eval_result.get("valid"):
            m = eval_result["metrics"]
            lines += [
                "## Metrics",
                f"- **MAE:** {m['mae']}",
                f"- **RMSE:** {m['rmse']}",
                f"- **R2:** {m['r2']}",
                "",
            ]
        output_path.write_text("\n".join(lines), encoding="utf-8")
        return output_path

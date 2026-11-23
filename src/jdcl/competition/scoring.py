"""Competition submission validation and scoring functions."""

from __future__ import annotations

from typing import Any, Dict, List

import numpy as np
import pandas as pd

from jdcl.models.baselines import regression_metrics


def validate_submission(
    submission_df: pd.DataFrame,
    expected_ids: pd.Series | List[str],
    schema: Dict[str, Any],
) -> List[str]:
    errors: List[str] = []
    id_col = schema.get("id_column", "record_id")
    if id_col not in submission_df.columns:
        errors.append(f"Submission missing id column '{id_col}'")
        return errors

    expected_list = list(expected_ids)
    if len(submission_df) != len(expected_list):
        errors.append(f"Row count mismatch: got {len(submission_df)}, expected {len(expected_list)}")

    if set(submission_df[id_col].astype(str)) != set(map(str, expected_list)):
        errors.append("Submission record_id set does not match evaluation split")

    for col, spec in schema.get("prediction_columns", {}).items():
        if col not in submission_df.columns:
            if not spec.get("nullable", False):
                errors.append(f"Missing required prediction column '{col}'")
            continue
        vals = pd.to_numeric(submission_df[col], errors="coerce")
        if not spec.get("nullable", False) and vals.isna().any():
            errors.append(f"Prediction column '{col}' contains NaN/non-numeric values")
        non_null = vals.dropna()
        if "min" in spec and len(non_null) > 0 and float(non_null.min()) < float(spec["min"]):
            errors.append(f"Prediction '{col}' min {non_null.min()} < {spec['min']}")
        if "max" in spec and len(non_null) > 0 and float(non_null.max()) > float(spec["max"]):
            errors.append(f"Prediction '{col}' max {non_null.max()} > {spec['max']}")
    return errors


def score_submission(
    ground_truth_df: pd.DataFrame,
    submission_df: pd.DataFrame,
    id_col: str = "record_id",
    target_col: str = "resolution_days",
) -> Dict[str, float]:
    merged = ground_truth_df[[id_col, target_col]].merge(
        submission_df[[id_col, "predicted_resolution_days"]],
        on=id_col,
        how="inner",
    )
    if len(merged) != len(ground_truth_df):
        raise ValueError("Submission IDs do not align 1-to-1 with ground truth")
    return regression_metrics(
        merged[target_col].to_numpy(dtype=float),
        merged["predicted_resolution_days"].to_numpy(dtype=float),
    )

"""Fairness diagnostics across protected and geographic groups."""

from __future__ import annotations

from typing import Any, Dict, List

import numpy as np
import pandas as pd


def compute_subgroup_fairness(
    df: pd.DataFrame,
    y_true_col: str,
    y_pred: np.ndarray,
    group_col: str,
) -> Dict[str, Any]:
    """Compute subgroup MAE, RMSE, and max subgroup MAE disparity."""
    if group_col not in df.columns:
        raise ValueError(f"Group column '{group_col}' not found")

    work = df[[group_col, y_true_col]].copy()
    work["y_pred"] = y_pred
    work["abs_err"] = np.abs(work[y_true_col] - work["y_pred"])
    work["sq_err"] = (work[y_true_col] - work["y_pred"]) ** 2

    subgroups: List[Dict[str, Any]] = []
    maes: List[float] = []
    for grp, gdf in work.groupby(group_col, observed=True):
        mae = float(gdf["abs_err"].mean())
        rmse = float(np.sqrt(gdf["sq_err"].mean()))
        maes.append(mae)
        subgroups.append(
            {
                "group": str(grp),
                "count": int(len(gdf)),
                "mean_actual": round(float(gdf[y_true_col].mean()), 3),
                "mean_predicted": round(float(gdf["y_pred"].mean()), 3),
                "mae": round(mae, 4),
                "rmse": round(rmse, 4),
            }
        )

    mae_gap = round(max(maes) - min(maes), 4) if maes else 0.0
    return {
        "group_column": group_col,
        "subgroups": subgroups,
        "max_mae_gap": mae_gap,
    }


def compute_sla_parity(
    df: pd.DataFrame,
    y_prob: np.ndarray,
    group_col: str,
    threshold: float = 0.5,
) -> Dict[str, Any]:
    """Compute positive prediction rate parity across subgroups."""
    work = df[[group_col]].copy()
    work["pred_pos"] = (y_prob >= threshold).astype(float)
    rates = work.groupby(group_col, observed=True)["pred_pos"].mean().to_dict()
    clean_rates = {str(k): round(float(v), 4) for k, v in rates.items()}
    vals = list(clean_rates.values())
    parity_ratio = round(min(vals) / max(max(vals), 1e-12), 4) if vals else 1.0
    return {
        "group_column": group_col,
        "positive_rates": clean_rates,
        "demographic_parity_ratio": parity_ratio,
    }

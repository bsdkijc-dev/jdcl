"""Build and execute all JDCL analytical notebooks, embedding verified outputs."""

from __future__ import annotations

import contextlib
import io
import json
from pathlib import Path
from typing import Any, Dict, List


ROOT = Path(__file__).resolve().parents[1]


def make_md_cell(text: str) -> Dict[str, Any]:
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": [line + "\n" for line in text.splitlines()],
    }


def make_code_cell(code: str, env: Dict[str, Any], exec_count: int) -> Dict[str, Any]:
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        exec(compile(code, "<notebook-cell>", "exec"), env)
    out = buf.getvalue()
    outputs = []
    if out:
        outputs.append(
            {
                "name": "stdout",
                "output_type": "stream",
                "text": [line + "\n" for line in out.rstrip("\n").splitlines()],
            }
        )
    return {
        "cell_type": "code",
        "execution_count": exec_count,
        "metadata": {},
        "outputs": outputs,
        "source": [line + "\n" for line in code.splitlines()],
    }


def save_notebook(path: Path, cells: List[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    nb = {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.11"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    path.write_text(json.dumps(nb, indent=2), encoding="utf-8")


def build_all() -> None:
    # 00_data_overview.ipynb
    env0: Dict[str, Any] = {}
    c0 = [
        make_md_cell(
            "# 00 — JFLM 2027 Synthetic Data Overview\n\n"
            "> **SYNTHETIC DATA DISCLAIMER:** 100% synthetic data (`SYNTHETIC_JFLM_2027_V1`). "
            "Contains NO real citizen identities or judicial records."
        ),
        make_code_cell(
            "import sys\nsys.path.insert(0, '../src')\nimport pandas as pd\n"
            "df = pd.read_csv('../data/synthetic/jflm_2027.csv')\n"
            "print('Shape:', df.shape)\n"
            "print('Data origins:', df['data_origin'].unique().tolist())\n"
            "print(df[['distance_to_court_km', 'travel_cost_idr_thousands', 'resolution_days', 'service_completed']].describe().round(2))",
            env0,
            1,
        ),
    ]
    save_notebook(ROOT / "notebooks" / "00_data_overview.ipynb", c0)

    # 01_exploratory_analysis.ipynb
    env1: Dict[str, Any] = {}
    c1 = [
        make_md_cell(
            "# 01 — Exploratory Analysis (Synthetic JFLM 2027)\n\n"
            "Explores synthetic correlations across `region_tier`, `service_channel`, and `vulnerability_group`. "
            "Correlations in synthetic data reflect modeling assumptions, not causal empirical claims."
        ),
        make_code_cell(
            "import pandas as pd\ndf = pd.read_csv('../data/synthetic/jflm_2027.csv')\n"
            "print('By Region Tier:')\n"
            "print(df.groupby('region_tier')[['distance_to_court_km', 'resolution_days', 'service_completed']].mean().round(2))\n"
            "print('\\nMissingness counts (zero-imputation preserved):')\n"
            "print(df.isna().sum()[df.isna().sum() > 0])",
            env1,
            1,
        ),
    ]
    save_notebook(ROOT / "notebooks" / "01_exploratory_analysis.ipynb", c1)

    # 02_baseline_model.ipynb
    env2: Dict[str, Any] = {}
    c2 = [
        make_md_cell(
            "# 02 — Baseline Models (Mean/Majority, Linear/Logistic, Random Forest)\n\n"
            "Uses deterministic 70/15/15 split with train-only preprocessing to prevent leakage."
        ),
        make_code_cell(
            "import sys\nsys.path.insert(0, '../src')\nimport pandas as pd\n"
            "from jdcl.models.baselines import (\n"
            "    deterministic_split, TabularPreprocessor, MeanMajorityBaseline,\n"
            "    RidgeLinearBaseline, LogisticBaseline, RandomForestBaseline,\n"
            "    regression_metrics, classification_and_calibration_metrics,\n"
            ")\n"
            "df = pd.read_csv('../data/synthetic/jflm_2027.csv')\n"
            "split = deterministic_split(df, seed=20270101)\n"
            "prep = TabularPreprocessor().fit(split.train_df)\n"
            "X_tr, X_val, X_te = prep.transform(split.train_df), prep.transform(split.val_df), prep.transform(split.test_df)\n"
            "y_tr, y_te = split.train_df['resolution_days'].to_numpy(float), split.test_df['resolution_days'].to_numpy(float)\n"
            "yc_tr, yc_te = split.train_df['service_completed'].to_numpy(int), split.test_df['service_completed'].to_numpy(int)\n"
            "m_mean = MeanMajorityBaseline().fit(y_tr, yc_tr)\n"
            "m_ridge = RidgeLinearBaseline(alpha=1.0).fit(X_tr, y_tr)\n"
            "m_rf = RandomForestBaseline(n_estimators=20, max_depth=6, seed=20270101).fit(X_tr, y_tr)\n"
            "m_log = LogisticBaseline().fit(X_tr, yc_tr)\n"
            "print('Test Regression — Mean:', regression_metrics(y_te, m_mean.predict(X_te)))\n"
            "print('Test Regression — Ridge:', regression_metrics(y_te, m_ridge.predict(X_te)))\n"
            "print('Test Regression — RandomForest:', regression_metrics(y_te, m_rf.predict(X_te)))\n"
            "print('Test Classification/Calibration — Logistic:', classification_and_calibration_metrics(yc_te, m_log.predict_proba(X_te)))",
            env2,
            1,
        ),
    ]
    save_notebook(ROOT / "notebooks" / "02_baseline_model.ipynb", c2)

    # 03_evaluation.ipynb
    env3: Dict[str, Any] = {}
    c3 = [
        make_md_cell(
            "# 03 — Evaluation, Calibration & Fairness Diagnostics\n\n"
            "Evaluates subgroup MAE disparity and demographic parity across `region_tier` and `vulnerability_group`."
        ),
        make_code_cell(
            "import sys\nsys.path.insert(0, '../src')\nimport pandas as pd\n"
            "from jdcl.models.baselines import deterministic_split, TabularPreprocessor, RandomForestBaseline, LogisticBaseline\n"
            "from jdcl.models.fairness import compute_subgroup_fairness, compute_sla_parity\n"
            "df = pd.read_csv('../data/synthetic/jflm_2027.csv')\n"
            "split = deterministic_split(df, seed=20270101)\n"
            "prep = TabularPreprocessor().fit(split.train_df)\n"
            "X_tr, X_te = prep.transform(split.train_df), prep.transform(split.test_df)\n"
            "rf = RandomForestBaseline(n_estimators=20, max_depth=6, seed=20270101).fit(X_tr, split.train_df['resolution_days'].to_numpy(float))\n"
            "log = LogisticBaseline().fit(X_tr, split.train_df['service_completed'].to_numpy(int))\n"
            "fair_reg = compute_subgroup_fairness(split.test_df, 'resolution_days', rf.predict(X_te), 'region_tier')\n"
            "fair_vuln = compute_subgroup_fairness(split.test_df, 'resolution_days', rf.predict(X_te), 'vulnerability_group')\n"
            "parity = compute_sla_parity(split.test_df, log.predict_proba(X_te), 'region_tier')\n"
            "print('Max MAE Gap (region_tier):', fair_reg['max_mae_gap'])\n"
            "print('Max MAE Gap (vulnerability_group):', fair_vuln['max_mae_gap'])\n"
            "print('SLA Demographic Parity Ratio (region_tier):', parity['demographic_parity_ratio'])",
            env3,
            1,
        ),
    ]
    save_notebook(ROOT / "notebooks" / "03_evaluation.ipynb", c3)

    # 04_policy_insights.ipynb
    env4: Dict[str, Any] = {}
    c4 = [
        make_md_cell(
            "# 04 — Policy Insights & Hypothesis Generation (Synthetic)\n\n"
            "> **IMPORTANT:** Findings below reflect **synthetic modeling assumptions** and "
            "**hypotheses requiring empirical validation**, NOT causal proof or real judicial performance."
        ),
        make_code_cell(
            "import pandas as pd\ndf = pd.read_csv('../data/synthetic/jflm_2027.csv')\n"
            "summary = df.groupby(['region_tier', 'service_channel'])[['resolution_days', 'service_completed']].mean().round(2)\n"
            "print(summary.head(12))",
            env4,
            1,
        ),
    ]
    save_notebook(ROOT / "notebooks" / "04_policy_insights.ipynb", c4)

    # kaggle/starter_notebook.ipynb
    env_k: Dict[str, Any] = {}
    ck = [
        make_md_cell(
            "# JFLM 2027 — Kaggle Community Competition Starter Notebook\n\n"
            "Generates a valid baseline submission (`predicted_resolution_days`) on the synthetic holdout split."
        ),
        make_code_cell(
            "import sys\nsys.path.insert(0, '../src')\nimport pandas as pd\n"
            "from jdcl.models.baselines import deterministic_split, TabularPreprocessor, RidgeLinearBaseline\n"
            "from jdcl.competition.engine import CompetitionEngine\n"
            "df = pd.read_csv('../data/synthetic/jflm_2027.csv')\n"
            "split = deterministic_split(df, seed=20270101)\n"
            "prep = TabularPreprocessor().fit(split.train_df)\n"
            "model = RidgeLinearBaseline().fit(prep.transform(split.train_df), split.train_df['resolution_days'].to_numpy(float))\n"
            "sub = pd.DataFrame({'record_id': split.test_df['record_id'], 'predicted_resolution_days': model.predict(prep.transform(split.test_df))})\n"
            "res = CompetitionEngine('jflm-2027').evaluate_submission(split.test_df, sub, sub)\n"
            "print('Valid:', res['valid'], '| Reproducible:', res['reproducible'], '| Metrics:', res['metrics'])",
            env_k,
            1,
        ),
    ]
    save_notebook(ROOT / "kaggle" / "starter_notebook.ipynb", ck)
    print("All 6 notebooks built and executed successfully.")


if __name__ == "__main__":
    build_all()

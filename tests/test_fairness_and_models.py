"""Tests for baseline models, calibration, and fairness metric calculations."""

import unittest

import numpy as np

from jdcl.data.generator import generate_jflm_2027_dataframe
from jdcl.models.baselines import (
    LogisticBaseline,
    MeanMajorityBaseline,
    RandomForestBaseline,
    RidgeLinearBaseline,
    TabularPreprocessor,
    classification_and_calibration_metrics,
    deterministic_split,
    regression_metrics,
)
from jdcl.models.fairness import compute_sla_parity, compute_subgroup_fairness


class TestFairnessAndModels(unittest.TestCase):
    def test_baselines_and_fairness(self) -> None:
        df = generate_jflm_2027_dataframe(n_rows=600, seed=20270101)
        split = deterministic_split(df, seed=20270101)
        prep = TabularPreprocessor().fit(split.train_df)
        X_tr = prep.transform(split.train_df)
        X_te = prep.transform(split.test_df)
        y_tr = split.train_df["resolution_days"].to_numpy(float)
        y_te = split.test_df["resolution_days"].to_numpy(float)
        yc_tr = split.train_df["service_completed"].to_numpy(int)
        yc_te = split.test_df["service_completed"].to_numpy(int)

        mean_m = MeanMajorityBaseline().fit(y_tr, yc_tr)
        ridge_m = RidgeLinearBaseline().fit(X_tr, y_tr)
        rf_m = RandomForestBaseline(n_estimators=10, max_depth=4, seed=20270101).fit(X_tr, y_tr)
        log_m = LogisticBaseline(n_iter=200).fit(X_tr, yc_tr)

        m_mean = regression_metrics(y_te, mean_m.predict(X_te))
        m_ridge = regression_metrics(y_te, ridge_m.predict(X_te))
        m_rf = regression_metrics(y_te, rf_m.predict(X_te))
        self.assertLess(m_ridge["mae"], m_mean["mae"])
        self.assertLess(m_rf["mae"], m_mean["mae"])

        cal = classification_and_calibration_metrics(yc_te, log_m.predict_proba(X_te))
        self.assertGreaterEqual(cal["accuracy"], 0.5)
        self.assertGreaterEqual(cal["ece"], 0.0)

        fair = compute_subgroup_fairness(split.test_df, "resolution_days", rf_m.predict(X_te), "region_tier")
        self.assertIn("max_mae_gap", fair)
        self.assertGreaterEqual(fair["max_mae_gap"], 0.0)

        parity = compute_sla_parity(split.test_df, log_m.predict_proba(X_te), "region_tier")
        self.assertGreaterEqual(parity["demographic_parity_ratio"], 0.0)
        self.assertLessEqual(parity["demographic_parity_ratio"], 1.0)


if __name__ == "__main__":
    unittest.main()

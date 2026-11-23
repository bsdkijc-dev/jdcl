"""Reproducible baseline models with leakage prevention and CPU-only fallbacks.

Includes:
- Majority / Mean baseline
- Linear Regression (OLS with Ridge L2 regularization) & Logistic Regression
- Random Forest Regressor (pure-NumPy bagged decision trees fallback if sklearn absent)
- Metrics: MAE, RMSE, R2, Accuracy, F1, Brier Score, Expected Calibration Error (ECE)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Tuple

import numpy as np
import pandas as pd


FEATURE_NUMERIC = [
    "distance_to_court_km",
    "travel_cost_idr_thousands",
    "digital_connectivity_index",
    "legal_aid_available",
    "fee_waiver_prodeo",
    "digital_intake_score",
    "paralegal_hours",
    "case_complexity_index",
]

FEATURE_CATEGORICAL = [
    "region_tier",
    "court_jurisdiction",
    "service_channel",
    "dispute_category",
    "vulnerability_group",
]


@dataclass
class SplitData:
    train_df: pd.DataFrame
    val_df: pd.DataFrame
    test_df: pd.DataFrame


def deterministic_split(
    df: pd.DataFrame,
    train_ratio: float = 0.70,
    val_ratio: float = 0.15,
    seed: int = 20270101,
) -> SplitData:
    """Deterministic row-shuffled split preventing leakage across splits."""
    rng = np.random.default_rng(seed)
    idx = np.arange(len(df))
    rng.shuffle(idx)
    n_train = int(len(df) * train_ratio)
    n_val = int(len(df) * val_ratio)
    return SplitData(
        train_df=df.iloc[idx[:n_train]].reset_index(drop=True),
        val_df=df.iloc[idx[n_train : n_train + n_val]].reset_index(drop=True),
        test_df=df.iloc[idx[n_train + n_val :]].reset_index(drop=True),
    )


class TabularPreprocessor:
    """Fit-on-train-only preprocessor to prevent data leakage."""

    def __init__(self) -> None:
        self.medians: Dict[str, float] = {}
        self.means: Dict[str, float] = {}
        self.stds: Dict[str, float] = {}
        self.categories: Dict[str, List[str]] = {}
        self.feature_names: List[str] = []

    def fit(self, df: pd.DataFrame) -> "TabularPreprocessor":
        for col in FEATURE_NUMERIC:
            s = pd.to_numeric(df[col], errors="coerce")
            med = float(s.median())
            self.medians[col] = med
            filled = s.fillna(med)
            self.means[col] = float(filled.mean())
            std = float(filled.std())
            self.stds[col] = std if std > 1e-8 else 1.0

        for col in FEATURE_CATEGORICAL:
            self.categories[col] = sorted(df[col].dropna().astype(str).unique().tolist())

        self.feature_names = list(FEATURE_NUMERIC)
        for col in FEATURE_CATEGORICAL:
            for cat in self.categories[col]:
                self.feature_names.append(f"{col}__{cat}")
        return self

    def transform(self, df: pd.DataFrame) -> np.ndarray:
        cols: List[np.ndarray] = []
        for col in FEATURE_NUMERIC:
            s = pd.to_numeric(df[col], errors="coerce").fillna(self.medians[col])
            arr = (s.to_numpy(dtype=float) - self.means[col]) / self.stds[col]
            cols.append(arr.reshape(-1, 1))
        for col in FEATURE_CATEGORICAL:
            vals = df[col].astype(str).to_numpy()
            for cat in self.categories[col]:
                cols.append((vals == cat).astype(float).reshape(-1, 1))
        return np.hstack(cols)


class MeanMajorityBaseline:
    def __init__(self) -> None:
        self.mean_days: float = 0.0
        self.pos_rate: float = 0.5

    def fit(self, y_reg: np.ndarray, y_cls: np.ndarray | None = None) -> "MeanMajorityBaseline":
        self.mean_days = float(np.mean(y_reg))
        if y_cls is not None:
            self.pos_rate = float(np.mean(y_cls))
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        return np.full(len(X), self.mean_days, dtype=float)

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        return np.full(len(X), self.pos_rate, dtype=float)


class RidgeLinearBaseline:
    def __init__(self, alpha: float = 1.0) -> None:
        self.alpha = alpha
        self.weights: np.ndarray | None = None
        self.bias: float = 0.0

    def fit(self, X: np.ndarray, y: np.ndarray) -> "RidgeLinearBaseline":
        Xb = np.hstack([np.ones((len(X), 1)), X])
        reg = self.alpha * np.eye(Xb.shape[1])
        reg[0, 0] = 0.0
        coef = np.linalg.solve(Xb.T @ Xb + reg, Xb.T @ y)
        self.bias = float(coef[0])
        self.weights = coef[1:]
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        assert self.weights is not None
        return np.clip(self.bias + X @ self.weights, 1.0, 365.0)


class LogisticBaseline:
    """L2-regularized logistic regression via gradient descent for SLA completion."""

    def __init__(self, lr: float = 0.1, n_iter: int = 400, l2: float = 1e-2) -> None:
        self.lr = lr
        self.n_iter = n_iter
        self.l2 = l2
        self.w: np.ndarray | None = None
        self.b: float = 0.0

    def fit(self, X: np.ndarray, y: np.ndarray) -> "LogisticBaseline":
        n, d = X.shape
        self.w = np.zeros(d, dtype=float)
        self.b = 0.0
        for _ in range(self.n_iter):
            z = np.clip(X @ self.w + self.b, -20.0, 20.0)
            p = 1.0 / (1.0 + np.exp(-z))
            err = p - y
            grad_w = (X.T @ err) / n + self.l2 * self.w
            grad_b = float(np.mean(err))
            self.w -= self.lr * grad_w
            self.b -= self.lr * grad_b
        return self

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        assert self.w is not None
        z = np.clip(X @ self.w + self.b, -20.0, 20.0)
        return 1.0 / (1.0 + np.exp(-z))


class _SimpleDecisionTreeRegressor:
    """Lightweight deterministic CART regressor for CPU-only environments."""

    def __init__(self, max_depth: int = 5, min_samples_leaf: int = 20, max_features: int | None = None) -> None:
        self.max_depth = max_depth
        self.min_samples_leaf = min_samples_leaf
        self.max_features = max_features
        self.tree: Dict[str, Any] | float = 0.0

    def _build(self, X: np.ndarray, y: np.ndarray, depth: int, rng: np.random.Generator) -> Dict[str, Any] | float:
        if depth >= self.max_depth or len(y) < 2 * self.min_samples_leaf or np.std(y) < 1e-6:
            return float(np.mean(y))

        n_features = X.shape[1]
        k = self.max_features or max(1, int(np.sqrt(n_features)))
        feat_idx = rng.choice(n_features, size=min(k, n_features), replace=False)

        best_mse = float("inf")
        best_split: Tuple[int, float] | None = None
        for f in feat_idx:
            col = X[:, f]
            thresholds = np.unique(np.quantile(col, [0.2, 0.4, 0.5, 0.6, 0.8]))
            for thr in thresholds:
                left = col <= thr
                n_left = int(left.sum())
                n_right = len(y) - n_left
                if n_left < self.min_samples_leaf or n_right < self.min_samples_leaf:
                    continue
                y_l, y_r = y[left], y[~left]
                mse = (n_left * np.var(y_l) + n_right * np.var(y_r)) / len(y)
                if mse < best_mse:
                    best_mse = mse
                    best_split = (int(f), float(thr))

        if best_split is None:
            return float(np.mean(y))

        f, thr = best_split
        left = X[:, f] <= thr
        return {
            "feature": f,
            "threshold": thr,
            "left": self._build(X[left], y[left], depth + 1, rng),
            "right": self._build(X[~left], y[~left], depth + 1, rng),
        }

    def fit(self, X: np.ndarray, y: np.ndarray, rng: np.random.Generator) -> "_SimpleDecisionTreeRegressor":
        self.tree = self._build(X, y, 0, rng)
        return self

    def _predict_row(self, row: np.ndarray, node: Dict[str, Any] | float) -> float:
        if isinstance(node, float):
            return node
        if row[node["feature"]] <= node["threshold"]:
            return self._predict_row(row, node["left"])
        return self._predict_row(row, node["right"])

    def predict(self, X: np.ndarray) -> np.ndarray:
        return np.array([self._predict_row(r, self.tree) for r in X], dtype=float)


class RandomForestBaseline:
    """Uses scikit-learn RandomForestRegressor if installed, else pure-NumPy bagged trees."""

    def __init__(self, n_estimators: int = 20, max_depth: int = 6, seed: int = 20270101) -> None:
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.seed = seed
        self._sklearn_model: Any = None
        self._trees: List[_SimpleDecisionTreeRegressor] = []

    def fit(self, X: np.ndarray, y: np.ndarray) -> "RandomForestBaseline":
        try:
            from sklearn.ensemble import RandomForestRegressor

            self._sklearn_model = RandomForestRegressor(
                n_estimators=self.n_estimators,
                max_depth=self.max_depth,
                random_state=self.seed,
                n_jobs=1,
            )
            self._sklearn_model.fit(X, y)
            return self
        except ImportError:
            rng = np.random.default_rng(self.seed)
            self._trees = []
            n = len(X)
            for _ in range(self.n_estimators):
                boot_idx = rng.integers(0, n, size=n)
                tree = _SimpleDecisionTreeRegressor(max_depth=self.max_depth, min_samples_leaf=20)
                tree.fit(X[boot_idx], y[boot_idx], rng)
                self._trees.append(tree)
            return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        if self._sklearn_model is not None:
            return np.clip(self._sklearn_model.predict(X), 1.0, 365.0)
        preds = np.mean([t.predict(X) for t in self._trees], axis=0)
        return np.clip(preds, 1.0, 365.0)


def regression_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
    err = y_true - y_pred
    mae = float(np.mean(np.abs(err)))
    rmse = float(np.sqrt(np.mean(err ** 2)))
    ss_res = float(np.sum(err ** 2))
    ss_tot = float(np.sum((y_true - np.mean(y_true)) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 1e-12 else 0.0
    return {"mae": round(mae, 4), "rmse": round(rmse, 4), "r2": round(r2, 4)}


def classification_and_calibration_metrics(
    y_true: np.ndarray,
    y_prob: np.ndarray,
    n_bins: int = 10,
) -> Dict[str, float]:
    y_pred = (y_prob >= 0.5).astype(int)
    acc = float(np.mean(y_pred == y_true))
    tp = int(np.sum((y_pred == 1) & (y_true == 1)))
    fp = int(np.sum((y_pred == 1) & (y_true == 0)))
    fn = int(np.sum((y_pred == 0) & (y_true == 1)))
    prec = tp / max(tp + fp, 1)
    rec = tp / max(tp + fn, 1)
    f1 = 2 * prec * rec / max(prec + rec, 1e-12)
    brier = float(np.mean((y_prob - y_true) ** 2))

    # Expected Calibration Error (ECE)
    bins = np.linspace(0.0, 1.0, n_bins + 1)
    ece = 0.0
    for i in range(n_bins):
        mask = (y_prob >= bins[i]) & (y_prob <= bins[i + 1] if i == n_bins - 1 else y_prob < bins[i + 1])
        if np.any(mask):
            ece += (np.sum(mask) / len(y_true)) * abs(float(np.mean(y_true[mask])) - float(np.mean(y_prob[mask])))

    return {
        "accuracy": round(acc, 4),
        "f1": round(f1, 4),
        "brier_score": round(brier, 4),
        "ece": round(float(ece), 4),
    }

"""JDCL v1.0 Local Streamlit Research Dashboard (Zero-Cost Local Mode)."""

from __future__ import annotations

from pathlib import Path
import sys

# Ensure src/ is importable when launched via `streamlit run app/dashboard.py`
SRC_DIR = Path(__file__).resolve().parents[1] / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

import pandas as pd
import streamlit as st

from jdcl.competition.registry import get_competition_metadata
from jdcl.config import PROJECT_ROOT, load_yaml
from jdcl.data.manifest import load_manifest
from jdcl.jpais.local_store import LocalJPAISStore
from jdcl.models.baselines import (
    MeanMajorityBaseline,
    RandomForestBaseline,
    RidgeLinearBaseline,
    TabularPreprocessor,
    deterministic_split,
    regression_metrics,
)
from jdcl.models.fairness import compute_subgroup_fairness
from jdcl.quality.validator import validate_dataset


st.set_page_config(page_title="JDCL v1.0 — JFLM 2027 Research Dashboard", layout="wide")

st.title("Justice Delivery Competition Lab (JDCL) v1.0")
st.subheader("Primary Initiative: Justice for the Last Mile Challenge 2027 (JFLM 2027)")

st.warning(
    "SYNTHETIC DATA DISCLAIMER: All data displayed in this dashboard is 100% deterministically "
    "generated synthetic data (`SYNTHETIC_JFLM_2027_V1`). It contains NO real citizen identities, "
    "NO real litigant records, and NO real judicial case performance."
)

csv_path = PROJECT_ROOT / "data" / "synthetic" / "jflm_2027.csv"
manifest_path = PROJECT_ROOT / "data" / "manifests" / "jflm_2027.yml"
schema_path = PROJECT_ROOT / "data" / "schemas" / "jflm_2027_schema.yml"

df = pd.read_csv(csv_path)
manifest = load_manifest(manifest_path)
schema = load_yaml(schema_path)
val_report = validate_dataset(df, schema=schema, manifest=manifest, csv_path=csv_path)
comp_meta = get_competition_metadata("jflm-2027")
jpais_store = LocalJPAISStore()
approval = jpais_store.check_publication_approval("jflm_2027_synthetic_v1")

tabs = st.tabs([
    "Dataset Overview",
    "Data Quality",
    "Baseline Performance",
    "Fairness Diagnostics",
    "Competition & Governance",
])

with tabs[0]:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Synthetic Rows", f"{len(df):,}")
    c2.metric("Columns", f"{len(df.columns)}")
    c3.metric("Mean Resolution (Days)", f"{df['resolution_days'].mean():.1f}")
    c4.metric("90-Day SLA Rate", f"{df['service_completed'].mean() * 100:.1f}%")
    st.dataframe(df.head(20), use_container_width=True)

with tabs[1]:
    st.write("### Automated Data Quality, Provenance & Privacy Checks")
    st.json(val_report.checks)
    if val_report.errors:
        st.error(val_report.errors)
    else:
        st.success("All required schema, null, duplicate, domain, provenance, and privacy checks passed.")

with tabs[2]:
    st.write("### CPU-Only Baseline Benchmarks (Synthetic Holdout Split)")
    split = deterministic_split(df)
    prep = TabularPreprocessor().fit(split.train_df)
    X_train = prep.transform(split.train_df)
    X_test = prep.transform(split.test_df)
    y_train = split.train_df["resolution_days"].to_numpy(dtype=float)
    y_test = split.test_df["resolution_days"].to_numpy(dtype=float)

    mean_m = MeanMajorityBaseline().fit(y_train)
    ridge_m = RidgeLinearBaseline().fit(X_train, y_train)
    rf_m = RandomForestBaseline(n_estimators=15, max_depth=5).fit(X_train, y_train)

    results = pd.DataFrame([
        {"Model": "Mean Baseline", **regression_metrics(y_test, mean_m.predict(X_test))},
        {"Model": "Ridge Linear Regression", **regression_metrics(y_test, ridge_m.predict(X_test))},
        {"Model": "Random Forest Baseline", **regression_metrics(y_test, rf_m.predict(X_test))},
    ])
    st.dataframe(results, use_container_width=True)

with tabs[3]:
    st.write("### Subgroup Fairness Diagnostics (Random Forest on Synthetic Test Split)")
    rf_preds = rf_m.predict(X_test)
    fair_region = compute_subgroup_fairness(split.test_df, "resolution_days", rf_preds, "region_tier")
    st.write(f"**Max Subgroup MAE Gap (`region_tier`):** {fair_region['max_mae_gap']} days")
    st.dataframe(pd.DataFrame(fair_region["subgroups"]), use_container_width=True)

with tabs[4]:
    st.write("### Competition Metadata & Publication Status")
    st.json(comp_meta)
    st.write("### Human Publication Approval Gate")
    st.info(
        f"Artifact: `{approval.artifact_id}` | Technical Checks Passed: `{val_report.passed}` | "
        f"Human Approved: `{approval.human_approved}` (External publishing remains blocked until human sign-off)"
    )

# Justice Delivery Competition Lab (JDCL) v1.0

**Primary Initiative:** Justice for the Last Mile Challenge 2027 (JFLM 2027)  
**Architecture Mandate:** Zero-Cost Community Mandate (`v1.0-ZC`)

> **SYNTHETIC DATA DISCLAIMER:** All datasets currently included in JDCL v1.0 (`data/synthetic/jflm_2027.csv`) are **100% deterministically generated synthetic data**. They contain **no real citizen identities, no real litigant records, and no real judicial case files**. Synthetic benchmark performance must **never** be interpreted as evidence of actual judicial service performance.

## Mission

Build an operational, reproducible, privacy-preserving, open-source competition and research infrastructure to discover better ways of delivering access to justice and judicial services to communities in Indonesia—without automating judicial decision-making and with zero additional financial expenditure.

## Repository Architecture

- `src/jdcl/`: Core Python package (synthetic data engine, data quality & privacy validator, baseline models & fairness diagnostics, competition engine, offline-first JPAIS interfaces).
- `data/`: Synthetic datasets (`data/synthetic/`), provenance manifests (`data/manifests/`), and formal schemas (`data/schemas/`).
- `notebooks/`: Five reproducible analytical notebooks (`00_data_overview.ipynb` through `04_policy_insights.ipynb`).
- `app/`: Local Streamlit research dashboard (`app/dashboard.py`).
- `kaggle/`: Kaggle Community Competition publication kit and guide.
- `docs/`: Governance framework, data dictionary, assumptions, policy research framework, outstanding issues, and human approval checklist.
- `reports/technical/`: Initial audit, publication readiness, and implementation reports.
- `.github/workflows/`: Free public-repo GitHub Actions for testing, data validation, docs checks, security scanning, and gated release preparation.
- `tests/`: Automated unit and integration test suite.

## Quickstart (Zero-Cost Local CPU)

```bash
# 1. Generate deterministic 10,000-row synthetic dataset and manifest
make generate

# 2. Run schema, null, duplicate, domain, outlier, provenance, and privacy checks
make validate

# 3. Run full automated test suite
make test

# 4. Launch local Streamlit research dashboard (requires optional streamlit install)
make dashboard
```

## Human Approval Gates

Automated pipelines **never** publish datasets, create GitHub releases, activate Kaggle competitions, or deploy public apps without explicit human authorization. See `docs/GOVERNANCE.md` and `docs/HUMAN_APPROVAL_CHECKLIST.md`.

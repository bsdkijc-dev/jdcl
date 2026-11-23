# Kaggle Publishing Guide (Zero-Cost Community Competition)

**Current Sandbox Limitation:** Kaggle API credentials (`~/.kaggle/kaggle.json`) and outbound network access are unavailable in the sandbox. All competition assets have been prepared locally in `kaggle/`.

## Human-Gated Publishing Steps (On Local Ubuntu Workstation)

1. Verify `reports/technical/PUBLICATION_READINESS_REPORT.md` and sign off on `docs/HUMAN_APPROVAL_CHECKLIST.md`.
2. Log in to Kaggle under the human owner's account (`judicialcollege`).
3. Navigate to **Competitions -> Host a Community Competition** (free tier only; never select Featured or paid promotion).
4. Copy metadata from `kaggle/competition_metadata.yml`, `kaggle/description.md`, `kaggle/evaluation_metric.md`, `kaggle/rules.md`, and `kaggle/faq.md`.
5. Upload `data/synthetic/jflm_2027.csv` as the competition dataset and configure the holdout evaluation split (`seed=20270101`).
6. Attach `kaggle/starter_notebook.ipynb` as the public starter notebook.

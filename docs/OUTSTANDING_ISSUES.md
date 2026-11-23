# JDCL v1.0 — Outstanding Issues Register

| ID | Category | Severity | Description | Status / Mitigation |
| :--- | :--- | :--- | :--- | :--- |
| **ISS-01** | Environment | Medium | `scikit-learn`, `duckdb`, `streamlit`, `jupyter`, `pytest`, and `kaggle` are not installed in the restricted offline sandbox. | Pure-NumPy/SciPy & `unittest` fallbacks implemented and executed; full `requirements.txt` ready for local `.venv` on Ubuntu workstation. |
| **ISS-02** | External Services | Info | No Kaggle API credentials (`kaggle.json`) or GitHub SSH keys in sandbox. | All Kaggle assets & GitHub Actions prepared locally; human-gated manual/local upload documented in `docs/KAGGLE_PUBLISHING_GUIDE.md`. |
| **ISS-03** | Data Provenance | Info | Dataset is 100% synthetic (`SYNTHETIC_JFLM_2027_V1`); no empirical court data integrated yet. | Intentional per Phase 2; empirical integration requires separate P1 public data ingestion & human ethics sign-off. |
| **ISS-04** | Dashboard Runtime | Low | `app/dashboard.py` syntax-verified via `py_compile`, but live Streamlit UI server not started in sandbox (package absent). | Run `make dashboard` inside local `.venv` on Ubuntu workstation to visually verify UI. |

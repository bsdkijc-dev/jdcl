# Challenge 02 — UMKM Justice Access & Enterprise Survival Analytics (Project 01)

## 1. Public Problem
Micro and small enterprises (UMK) face disproportionate procedural and financial barriers when enforcing contracts or resolving commercial disputes.

## 2. Research Question
How does access to justice—measured by dispute resolution timelines, procedural clarity, and local court access—affect the survival and growth of Indonesian UMKs?

## 3. Measurable Objective
Quantify district-level justice bottlenecks and produce reproducible policy elasticity models without imputing missing official records.

## 4. Verified & Synthetic Dataset
- Empirical `DS05` (`ds05_umkm_economic_indicators.csv`, 278 records) and `DS09` (`ds09_legal_information_register.csv`, 11 regulations) from `judicialcollege/justice-for-umkm-synthetic-pilot-v1`, paired with synthetic `DS01`/`DS06`/`DS07` pilot tables.

## 5. Reproducible Methodology
Zero-imputation DuckDB/Pandas aggregation and Scikit-learn regression baseline preserving explicit completeness flags (`baseline/umkm_baseline.py`).

## 6. Participant Instructions
1. Load `DS05`, `DS09`, and synthetic `DS01`/`DS06`/`DS07` in a reproducible notebook.
2. Compute district-level completeness and survival indicators without converting `NULL` to `0`.
3. Submit a public Kaggle Notebook and a 2-page Markdown policy brief.

## 7. Evaluation Criteria
- Empirical Rigor & Zero-Imputation Compliance: 35%
- Reproducibility: 25%
- Actionable Policy Clarity: 25%
- Documentation Quality: 15%

## 8. Submission Requirements
Kaggle Notebook URL (or `.ipynb`), policy brief `.md`, and exact dataset provenance citations.

## 9. Ethical & Privacy Safeguards
Aggregated district indicators and synthetic case rows only; zero business-owner PII; no individual case outcome prediction.

## 10. Open-Source Output Strategy
CC-BY-4.0 notebooks and policy synthesis merged into `bsdkijc-dev/justice-for-umkm-observatory` after human review.

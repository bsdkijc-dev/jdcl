# JDCL v1.0 — Publication Readiness Report

**Artifact Evaluated:** `data/synthetic/jflm_2027.csv` (`jflm_2027_synthetic_v1`)  
**Assessment Date:** 2026-11-23  
**Notice:** A successful technical validation is **NOT** publication authorization.

## 1. Data Classification

- **Class:** `P1_SYNTHETIC_PUBLIC_CANDIDATE`
- **Nature:** 100% deterministically generated synthetic data (`SYNTHETIC_JFLM_2027_V1`).

## 2. Provenance Verification

- **Manifest:** `data/manifests/jflm_2027.yml`
- **SHA-256 Checksum:** Verified (`e08685444d57...`) against `data/synthetic/jflm_2027.csv`.
- **Seed & Reproducibility:** `seed=20270101`, `10,000` rows × `19` columns; bit-for-bit reproducible.

## 3. Privacy Assessment

- **Prohibited PII Columns:** None present (`nik`, `full_name`, `address`, `phone`, `email`, `case_number`, `judge_name`, `litigant_name` all absent).
- **Regex PII Scan:** `0` hits across string columns.
- **Real Judicial Records:** `0` (strictly synthetic).

## 4. Licence Verification

- **Code & Documentation:** Apache-2.0 (`pyproject.toml`).
- **Synthetic Dataset:** `CC0-1.0 / Apache-2.0` (`data/manifests/jflm_2027.yml`).

## 5. Security Scan

- No `.env`, `kaggle.json`, private keys, or API secrets present in the repository.
- `.gitignore` explicitly excludes `.env`, `kaggle.json`, `*.pem`, `*.key`.
- `config/settings.yml` enforces `allow_external_publish: false` and `allow_kaggle_activation: false`.

## 6. Reproducibility Results

- `python3 -m jdcl.quality.validator`: 8/8 checks `PASS`.
- `python3 -m unittest discover -s tests`: 14/14 tests `OK` (`0.384s`).
- All 6 notebooks (`00_data_overview.ipynb` through `04_policy_insights.ipynb` + `kaggle/starter_notebook.ipynb`) executed cleanly.

## 7. Human Approval Status

- **Status:** **PENDING EXPLICIT HUMAN AUTHORIZATION** (see `docs/HUMAN_APPROVAL_CHECKLIST.md`).
- No external upload, GitHub release, or Kaggle competition activation has been performed.

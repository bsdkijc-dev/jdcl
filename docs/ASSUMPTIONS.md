# JDCL v1.0 — Documented Assumptions

All assumptions below are recorded to maintain strict transparency between **synthetic assumptions** and **empirical observations** in accordance with JDCL Operating Principles.

## 1. Domain & Synthetic Data Assumptions (JFLM 2027)

1. **Geographic Scope (Synthetic Representation):** Synthetic records represent district-level/sub-district access-to-justice scenarios across representative Indonesian province tiers (e.g., `Jawa Barat`, `Jawa Tengah`, `Jawa Timur`, `Nusa Tenggara Barat`, `Nusa Tenggara Timur`, `Sumatera Utara`, `Sulawesi Selatan`, `Papua`, `Maluku`, `Kalimantan Tengah`) with urban, peri-urban, rural, and remote/archipelagic (`3T`) classifications. Distributions are **synthetic modeling assumptions**, not official BPS or Mahkamah Agung statistics.
2. **Case & Service Categories:** Synthetic disputes cover civil/small-claims, family/religious court matters, land/agrarian disputes, labor/industrial relations, and administrative/legal-aid consultations—represented strictly as abstract categorical codes without real case numbers or personal identifiers.
3. **Target Variable (`resolution_days` & `service_completed`):**
   - `resolution_days` (continuous, bounded `[1, 365]`) models synthetic end-to-end service delivery duration from intake to resolution.
   - `service_completed` (binary `0/1`) models whether the legal aid / last-mile justice service was completed within target SLA (`<= 90` days) without abandonment.
   - Relationships between distance to court, digital connectivity, legal aid availability, fee-waiver (`prodeo`) eligibility, and resolution time are **synthetic structural equations** with controlled Gaussian noise—not empirical causal estimates.
4. **Zero-Imputation & Missingness:** Controlled synthetic missingness (~1.5%–3% in non-key optional operational fields such as `digital_intake_score` or `paralegal_hours`) is preserved as empty/NaN rather than imputed to zero, matching JPAIS data hygiene standards.

## 2. Technical & Zero-Cost Infrastructure Assumptions

5. **Zero-Cost Mandate (`v1.0-ZC`):** All tooling uses free, open-source Python packages, GitHub Free public-repo Actions, GitHub Pages / Streamlit Community Cloud, and Kaggle Community Competitions.
6. **CPU-Only & Sandbox Compatibility:** Baseline models (`Majority/Mean`, `Linear/Logistic Regression`, `Random Forest`) include pure-NumPy/SciPy implementations so that all training, evaluation, and tests run deterministically on CPU without requiring GPU rentals or external APIs. When `scikit-learn` is available on the local Ubuntu workstation, identical interfaces apply.
7. **Test Runner Compatibility:** Test files are written in standard `pytest` / `unittest` style so they execute identically under `python3 -m unittest` (in restricted environments) and `pytest` (in CI and local `.venv`).
8. **Offline-First JPAIS Integration:** JPAIS interfaces operate against a local JSON/YAML file store (`artifacts/jpais_store/` or configurable path) by default, requiring zero live API endpoints or credentials.

## 3. Governance & Publication Assumptions

9. **Data Classification:** All JFLM 2027 synthetic outputs are classified as `P1_SYNTHETIC_PUBLIC_CANDIDATE` (no PII, no real judicial records), yet external upload to Kaggle or GitHub remains **blocked pending explicit human authorization**.
10. **Human Authority:** No automated workflow or agent action may activate a Kaggle competition, publish a GitHub release, or claim institutional endorsement by Mahkamah Agung RI or any Indonesian government body.

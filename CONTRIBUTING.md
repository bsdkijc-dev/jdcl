# JDCL Open-Source Contribution Guidelines

Welcome to the **Justice Delivery Competition Lab (JDCL) — Zero-Cost Community Edition (`v1.0-ZC`)**.

## 1. Mission & Attribution
JDCL is an independent public-interest innovation laboratory. Contributions are licensed under **MIT / Apache-2.0** (code) and **CC-BY-4.0** (datasets and documentation). Community contributions do **not** represent official institutional endorsements by Mahkamah Agung RI, Kaggle, or any partner university.

## 2. Zero-Cost & Reproducibility Rules
- All baselines and submissions must run on **zero-cost open-source tools** (Python, DuckDB, Pandas, Scikit-learn, JupyterLab) and free-tier quotas.
- Do **not** introduce paid APIs, paid cloud runners, or proprietary dependencies.
- Include deterministic seeds and a `README.md` with exact reproduction commands.

## 3. Data Hygiene & Governance
- **Zero Imputation:** Never convert missing values to `0` or impute missing official figures; retain empty cells with explicit completeness flags.
- **Zero PII:** Exclude all personal identifiers of judges, litigants, or court staff.
- **Source Access:** Do not submit automated scrapers targeting WAF-protected portals (`putusan3.mahkamahagung.go.id` HTTP 403). Use approved public datasets or synthetic pilots.

## 4. Pull Request Checklist
1. Pass `python3 -m unittest discover -s tests -p "test_*.py"`.
2. Pass all `challenges/*/tests/test_*.py` suites.
3. Verify `dataset-metadata.json` title (6–50 chars) and subtitle (20–80 chars).

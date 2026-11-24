# Challenge 03 — Open Judicial Metadata & Accessibility Tooling Hackathon (Projects 02 & 05)

## 1. Public Problem
Empirical audits in IOJO (2024–2025) show 69.09% metadata completeness and 62.73% source verifiability across annual judicial reports, while 684 court satkers await address/registry verification.

## 2. Research Question
What reusable, zero-cost open-source tools can standardize Indonesian court metadata, validate schema completeness, and improve public legal information search?

## 3. Measurable Objective
Deliver passing open-source CLI validators, crosswalk mappers, or static-site search prototypes deployable at Rp 0 on GitHub Pages.

## 4. Verified & Synthetic Dataset
- `IOJO` DS02/DS06 (290 rows), `Master Court Registry` (891 courts, 358 DIPA codes), and `JRC` NTB/Jawa Barat court & OBH tables.

## 5. Reproducible Methodology
Python schema validation (`baseline/validate_metadata.py`) and static JSON/DuckDB search indexing with zero backend hosting cost.

## 6. Participant Instructions
1. Fork `bsdkijc-dev/jdcl` and extend `challenges/03-open-metadata/baseline/validate_metadata.py` or add a static search tool.
2. Include `unittest` tests and a `README.md` with local setup steps.
3. Submit a Pull Request passing GitHub Actions CI.

## 7. Evaluation Criteria
- Code Quality & Test Pass Rate: 35%
- Zero-Cost Deployability: 25%
- Public Accessibility Impact: 25%
- Documentation Quality: 15%

## 8. Submission Requirements
GitHub Pull Request passing CI, MIT/Apache-2.0 license, and reproducible local usage example.

## 9. Ethical & Privacy Safeguards
Institutional satker metadata only; zero personal staff or judge data; no automated scraping of WAF-blocked portals.

## 10. Open-Source Output Strategy
Merged into the JDCL/IOJO open-source toolkit and statically hosted via GitHub Pages upon human approval.

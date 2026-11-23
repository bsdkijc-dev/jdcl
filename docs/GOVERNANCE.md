# JDCL v1.0 — Governance, Ethics & Responsible AI Framework

## 1. Core Mandate & Zero-Cost Principle

The Justice Delivery Competition Lab (JDCL) operates under the **Zero-Cost Community Mandate (`v1.0-ZC`)**: all research, competitions, hosting, and software tooling must remain free, open-source, and community-accessible without paid cloud services, paid APIs, or cash prize pools.

## 2. Non-Automation of Judicial Decision-Making

- JDCL models **service delivery logistics** (e.g., expected resolution duration, intake accessibility, resource allocation bottlenecks, legal-aid coverage).
- JDCL **strictly prohibits** predicting judicial verdicts, sentencing, liability, or automating any judicial decision-making.

## 3. Data Classification & Privacy Safeguards

| Class | Label | External Publication | Description |
| :--- | :--- | :--- | :--- |
| **P1** | Public Synthetic / Open | Allowed **only with human approval** | Verified synthetic datasets, open-source code, public documentation |
| **P2** | Internal Research | Prohibited | Draft analyses, unvalidated experiments |
| **P3** | Restricted Institutional | Prohibited | Non-public administrative data (not stored in JDCL) |
| **P4** | Sensitive / PII | Strictly Prohibited | Litigant, citizen, or staff identifiers |
| **P5** | Prohibited | Strictly Prohibited | Sealed/confidential court records |

Every dataset must pass automated PII-column and pattern checks before validation succeeds.

## 4. Three-Tier Human Authority Model

1. **Level 1 (Autonomous Local):** Synthetic data generation, local schema/quality validation, baseline model training, unit testing, local documentation.
2. **Level 2 (Human Review Required):** Policy recommendation framing, competition rule revisions, fairness threshold adjustments.
3. **Level 3 (Explicit Human Authorization Required):**
   - Publishing or uploading datasets to Kaggle or GitHub.
   - Creating or activating a Kaggle Community Competition.
   - Publishing GitHub releases or changing repository visibility.
   - Deploying any public Streamlit/GitHub Pages site.
   - Any institutional representation or external communication.

# JDCL Human-Approval Launch Packet (Challenges 01–03)

Status: **READY FOR HUMAN REVIEW — NOT PUBLISHED (v1.0-ZC)**

| Challenge | Kaggle Dataset ID | CSV Rows | Pre-Flight Gate |
| :--- | :--- | ---: | :--- |
| `01-legal-ai` | `judicialcollege/jdcl-legal-ai-citation-benchmark` | 2012 | PASS |
| `02-umkm-justice` | `judicialcollege/jdcl-umkm-justice-survival-challenge` | 60 | PASS |
| `03-open-metadata` | `judicialcollege/jdcl-open-judicial-metadata-toolkit` | 80 | PASS |

## Mandatory Human Sign-Off Checklist
1. Review `reports/week4_preflight_audit.json` (`all_passed: true`).
2. Run `bash scripts/stage_kaggle_private.sh` to upload datasets as **Private**.
3. Inspect each Private dataset & starter notebook on `kaggle.com/judicialcollege`.
4. Explicitly approve before switching visibility to Public or launching competitions.

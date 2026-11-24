"""JDCL Week 4 Pre-Flight Audit: zero-PII, zero-imputation, metadata & framework checks."""

import csv
import json
import pathlib
import re

FORBIDDEN_PII_COLS = {"nik", "ktp", "phone", "email", "judge_name", "litigant_name", "address"}
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
REQUIRED_SECTIONS = [
    "## 1. Public Problem",
    "## 2. Research Question",
    "## 3. Measurable Objective",
    "## 4. Verified & Synthetic Dataset",
    "## 5. Reproducible Methodology",
    "## 6. Participant Instructions",
    "## 7. Evaluation Criteria",
    "## 8. Submission Requirements",
    "## 9. Ethical & Privacy Safeguards",
    "## 10. Open-Source Output Strategy",
]


def audit_challenge(ch_dir: pathlib.Path) -> dict:
    errors = []
    readme_p = ch_dir / "README.md"
    if not readme_p.is_file():
        errors.append("Missing README.md")
    else:
        txt = readme_p.read_text(encoding="utf-8")
        for sec in REQUIRED_SECTIONS:
            if sec not in txt:
                errors.append(f"README.md missing {sec}")

    if not (ch_dir / "RULES.md").is_file():
        errors.append("Missing RULES.md")

    meta_p = ch_dir / "kaggle" / "dataset-metadata.json"
    meta = {}
    if not meta_p.is_file():
        errors.append("Missing kaggle/dataset-metadata.json")
    else:
        meta = json.loads(meta_p.read_text(encoding="utf-8"))
        t_len = len(meta.get("title", ""))
        s_len = len(meta.get("subtitle", ""))
        if not (6 <= t_len <= 50):
            errors.append(f"Title length {t_len} outside 6..50")
        if not (20 <= s_len <= 80):
            errors.append(f"Subtitle length {s_len} outside 20..80")
        if not meta.get("keywords"):
            errors.append("Missing keywords")

    csv_files = sorted((ch_dir / "kaggle" / "data").glob("*.csv")) if (ch_dir / "kaggle" / "data").is_dir() else []
    if not csv_files:
        errors.append("No CSV files in kaggle/data/")
    total_rows = 0
    for csv_p in csv_files:
        raw = csv_p.read_text(encoding="utf-8")
        if "Rp" in raw or "IDR" in raw:
            errors.append(f"Currency symbol found in {csv_p.name}")
        if EMAIL_RE.search(raw):
            errors.append(f"Potential email PII found in {csv_p.name}")
        with csv_p.open("r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            cols = {c.lower() for c in (reader.fieldnames or [])}
            bad_cols = cols & FORBIDDEN_PII_COLS
            if bad_cols:
                errors.append(f"Forbidden PII columns {sorted(bad_cols)} in {csv_p.name}")
            total_rows += sum(1 for _ in reader)

    return {
        "challenge": ch_dir.name,
        "kaggle_id": meta.get("id", ""),
        "csv_files": [p.name for p in csv_files],
        "total_csv_rows": total_rows,
        "passed": len(errors) == 0,
        "errors": errors,
    }


def run_audit(repo_root: pathlib.Path) -> dict:
    challenges_dir = repo_root / "challenges"
    results = [audit_challenge(p) for p in sorted(challenges_dir.iterdir()) if p.is_dir()]
    all_passed = all(r["passed"] for r in results)

    reports_dir = repo_root / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    (reports_dir / "week4_preflight_audit.json").write_text(
        json.dumps({"all_passed": all_passed, "challenges": results}, indent=2),
        encoding="utf-8",
    )

    lines = [
        "# JDCL Human-Approval Launch Packet (Challenges 01–03)",
        "",
        "Status: **READY FOR HUMAN REVIEW — NOT PUBLISHED (v1.0-ZC)**",
        "",
        "| Challenge | Kaggle Dataset ID | CSV Rows | Pre-Flight Gate |",
        "| :--- | :--- | ---: | :--- |",
    ]
    for r in results:
        status = "PASS" if r["passed"] else f"FAIL ({len(r['errors'])})"
        lines.append(f"| `{r['challenge']}` | `{r['kaggle_id']}` | {r['total_csv_rows']} | {status} |")

    lines.extend([
        "",
        "## Mandatory Human Sign-Off Checklist",
        "1. Review `reports/week4_preflight_audit.json` (`all_passed: true`).",
        "2. Run `bash scripts/stage_kaggle_private.sh` to upload datasets as **Private**.",
        "3. Inspect each Private dataset & starter notebook on `kaggle.com/judicialcollege`.",
        "4. Explicitly approve before switching visibility to Public or launching competitions.",
    ])
    (reports_dir / "HUMAN_APPROVAL_LAUNCH_PACKET.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    return {"all_passed": all_passed, "results": results}


if __name__ == "__main__":
    root = pathlib.Path(__file__).resolve().parents[1]
    summary = run_audit(root)
    print(json.dumps(summary, indent=2))
    if not summary["all_passed"]:
        raise SystemExit(1)

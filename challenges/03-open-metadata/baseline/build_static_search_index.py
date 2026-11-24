"""Zero-cost metadata completeness auditor & static GitHub Pages search index builder."""

import csv
import json
import pathlib


def build_index(input_csv: pathlib.Path, audit_csv: pathlib.Path, index_json: pathlib.Path) -> dict:
    with input_csv.open("r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    by_branch: dict[str, list[dict]] = {}
    search_entries = []

    for r in rows:
        by_branch.setdefault(r["branch"], []).append(r)
        search_entries.append({
            "id": r["satker_id"],
            "name": r["court_name"],
            "branch": r["branch"],
            "province": r["province_code"],
            "verified": r["verification_status"] == "VERIFIED",
        })

    audit_csv.parent.mkdir(parents=True, exist_ok=True)
    with audit_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["branch", "total_courts", "verified_courts", "dipa_completeness_pct"])
        for branch, b_rows in sorted(by_branch.items()):
            verified = sum(1 for r in b_rows if r["verification_status"] == "VERIFIED")
            dipa_present = sum(1 for r in b_rows if r["dipa_code"] not in ("", "NULL", None))
            pct = round((dipa_present / len(b_rows)) * 100, 2)
            writer.writerow([branch, len(b_rows), verified, pct])

    index_json.parent.mkdir(parents=True, exist_ok=True)
    index_json.write_text(json.dumps({"count": len(search_entries), "items": search_entries}, indent=2), encoding="utf-8")

    return {"branches": len(by_branch), "indexed_courts": len(search_entries)}


if __name__ == "__main__":
    base = pathlib.Path(__file__).resolve().parents[1]
    res = build_index(
        base / "kaggle" / "data" / "satker_registry_sample.csv",
        base / "baseline" / "completeness_audit.csv",
        base / "baseline" / "static_search_index.json",
    )
    print("Open Metadata Baseline:", res)

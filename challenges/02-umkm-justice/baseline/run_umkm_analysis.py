"""Zero-imputation district aggregation & survival correlation baseline (Challenge 02)."""

import csv
import math
import pathlib
import statistics


def pearson_r(xs: list[float], ys: list[float]) -> float:
    if len(xs) < 2 or len(xs) != len(ys):
        return 0.0
    mx, my = statistics.mean(xs), statistics.mean(ys)
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    den_x = math.sqrt(sum((x - mx) ** 2 for x in xs))
    den_y = math.sqrt(sum((y - my) ** 2 for y in ys))
    if den_x == 0 or den_y == 0:
        return 0.0
    return round(num / (den_x * den_y), 4)


def run_analysis(input_csv: pathlib.Path, output_csv: pathlib.Path) -> dict:
    with input_csv.open("r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    by_prov: dict[str, list[dict]] = {}
    xs_days, ys_surv = [], []

    for r in rows:
        by_prov.setdefault(r["province_name"], []).append(r)
        if r["avg_dispute_days"] not in ("", "NULL", None):
            xs_days.append(float(r["avg_dispute_days"]))
            ys_surv.append(float(r["survival_rate_pct"]))

    output_csv.parent.mkdir(parents=True, exist_ok=True)
    with output_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "province_name", "district_count", "dispute_days_completeness",
            "mean_survival_rate_pct", "mean_dispute_days",
        ])
        for prov, p_rows in sorted(by_prov.items()):
            valid_days = [float(r["avg_dispute_days"]) for r in p_rows if r["avg_dispute_days"] not in ("", "NULL", None)]
            surv_vals = [float(r["survival_rate_pct"]) for r in p_rows]
            completeness = round(len(valid_days) / len(p_rows), 4)
            mean_days = round(statistics.mean(valid_days), 2) if valid_days else ""
            mean_surv = round(statistics.mean(surv_vals), 2)
            writer.writerow([prov, len(p_rows), completeness, mean_surv, mean_days])

    return {
        "provinces": len(by_prov),
        "total_districts": len(rows),
        "complete_dispute_rows": len(xs_days),
        "dispute_days_vs_survival_r": pearson_r(xs_days, ys_surv),
    }


if __name__ == "__main__":
    base = pathlib.Path(__file__).resolve().parents[1]
    res = run_analysis(base / "kaggle" / "data" / "umkm_justice_pilot.csv", base / "baseline" / "umkm_district_summary.csv")
    print("UMKM Baseline Summary:", res)

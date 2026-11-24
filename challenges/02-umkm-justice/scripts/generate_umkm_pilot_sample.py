"""Deterministic zero-imputation synthetic UMKM justice pilot generator (v1.0-ZC)."""

import csv
import pathlib
import random

SEED = 20270301
VERSION_TAG = "SYNTHETIC_JDCL_UMKM_V1"

PROVINCES = [
    ("32", "Jawa Barat"),
    ("33", "Jawa Tengah"),
    ("35", "Jawa Timur"),
    ("52", "Nusa Tenggara Barat"),
    ("73", "Sulawesi Selatan"),
]


def generate_umkm_pilot(output_dir: pathlib.Path, seed: int = SEED, n_districts: int = 60) -> dict:
    rng = random.Random(seed)
    output_dir.mkdir(parents=True, exist_ok=True)
    out_csv = output_dir / "umkm_justice_pilot.csv"

    missing_duration = 0
    with out_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "district_id", "province_code", "province_name",
            "umkm_count", "survival_rate_pct", "avg_dispute_days",
            "procedural_clarity_score", "dataset_tag",
        ])
        for i in range(1, n_districts + 1):
            prov_code, prov_name = PROVINCES[(i - 1) % len(PROVINCES)]
            umkm_count = rng.randint(1200, 45000)
            survival_rate = round(rng.uniform(68.0, 94.5), 2)
            # 20% missing dispute duration — retained as empty cell (zero imputation)
            if i % 5 == 0:
                dispute_days = ""
                missing_duration += 1
            else:
                dispute_days = round(rng.uniform(28.0, 145.0), 1)
            clarity = round(rng.uniform(0.45, 0.92), 3)
            writer.writerow([
                f"DIST_{prov_code}_{i:03d}", prov_code, prov_name,
                umkm_count, survival_rate, dispute_days, clarity, VERSION_TAG,
            ])

    return {
        "rows": n_districts,
        "missing_dispute_days": missing_duration,
        "output_csv": str(out_csv),
    }


if __name__ == "__main__":
    out = pathlib.Path(__file__).resolve().parents[1] / "kaggle" / "data"
    print(generate_umkm_pilot(out))

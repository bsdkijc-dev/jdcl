"""Deterministic synthetic court satker metadata sample modeled on IOJO & Master Court Registry."""

import csv
import pathlib
import random

SEED = 20270302
VERSION_TAG = "SYNTHETIC_JDCL_METADATA_V1"

BRANCHES = ["PN", "PA", "PTUN", "DILMIL"]


def generate_metadata_sample(output_dir: pathlib.Path, seed: int = SEED, n_courts: int = 80) -> dict:
    rng = random.Random(seed)
    output_dir.mkdir(parents=True, exist_ok=True)
    out_csv = output_dir / "satker_registry_sample.csv"

    pending = 0
    with out_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "satker_id", "court_name", "branch", "province_code",
            "dipa_code", "verification_status", "dataset_tag",
        ])
        for i in range(1, n_courts + 1):
            branch = BRANCHES[(i - 1) % len(BRANCHES)]
            prov_code = rng.choice(["32", "33", "35", "52", "73"])
            if i % 4 == 0:
                dipa = ""
                status = "PENDING_VERIFICATION"
                pending += 1
            else:
                dipa = f"{400000 + i:06d}"
                status = "VERIFIED"
            writer.writerow([
                f"MA-COURT-{i:04d}", f"{branch} Sample {i:03d}", branch,
                prov_code, dipa, status, VERSION_TAG,
            ])

    return {"courts": n_courts, "pending_verification": pending, "output_csv": str(out_csv)}


if __name__ == "__main__":
    out = pathlib.Path(__file__).resolve().parents[1] / "kaggle" / "data"
    print(generate_metadata_sample(out))

"""Comprehensive data quality, schema, provenance, and privacy validator."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List

import numpy as np
import pandas as pd

from jdcl.config import load_yaml
from jdcl.data.manifest import compute_sha256, load_manifest


PII_PATTERNS = [
    re.compile(r"\b\d{16}\b"),  # Indonesian NIK 16-digit pattern
    re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"),  # Email
    re.compile(r"\b(?:\+62|08)\d{8,12}\b"),  # Indonesian phone number
]


@dataclass
class ValidationReport:
    passed: bool
    checks: Dict[str, bool] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "passed": self.passed,
            "checks": self.checks,
            "errors": self.errors,
            "warnings": self.warnings,
            "metrics": self.metrics,
        }


def validate_dataset(
    df: pd.DataFrame,
    schema: Dict[str, Any],
    manifest: Dict[str, Any] | None = None,
    csv_path: Path | None = None,
) -> ValidationReport:
    errors: List[str] = []
    warnings: List[str] = []
    checks: Dict[str, bool] = {}

    # 1. Schema & Column Presence
    expected_cols = list(schema.get("columns", {}).keys())
    actual_cols = list(df.columns)
    missing_cols = [c for c in expected_cols if c not in actual_cols]
    extra_cols = [c for c in actual_cols if c not in expected_cols]
    checks["schema_columns"] = len(missing_cols) == 0 and len(extra_cols) == 0
    if missing_cols:
        errors.append(f"Missing required columns: {missing_cols}")
    if extra_cols:
        errors.append(f"Unexpected extra columns: {extra_cols}")

    # 2. Duplicate Detection (primary key + full-row)
    pk = schema.get("primary_key", "record_id")
    pk_dups = int(df[pk].duplicated().sum()) if pk in df.columns else 0
    row_dups = int(df.duplicated().sum())
    checks["duplicate_detection"] = pk_dups == 0 and row_dups == 0
    if pk_dups > 0:
        errors.append(f"Primary key '{pk}' has {pk_dups} duplicates")
    if row_dups > 0:
        errors.append(f"Dataset has {row_dups} exact duplicate rows")

    # 3. Null-value & Domain Validation
    null_ok = True
    domain_ok = True
    null_rates: Dict[str, float] = {}
    for col, spec in schema.get("columns", {}).items():
        if col not in df.columns:
            continue
        series = df[col]
        null_count = int(series.isna().sum())
        null_rate = float(null_count / max(len(df), 1))
        null_rates[col] = round(null_rate, 5)

        if not spec.get("nullable", True) and null_count > 0:
            null_ok = False
            errors.append(f"Non-nullable column '{col}' contains {null_count} nulls")
        max_null = spec.get("max_null_rate")
        if max_null is not None and null_rate > float(max_null):
            null_ok = False
            errors.append(f"Column '{col}' null rate {null_rate:.4f} exceeds max {max_null}")

        non_null = series.dropna()
        if "allowed_values" in spec:
            allowed = set(spec["allowed_values"])
            invalid = set(non_null.unique()) - allowed
            if invalid:
                domain_ok = False
                errors.append(f"Column '{col}' has invalid values: {sorted(map(str, invalid))[:5]}")
        if "min" in spec and len(non_null) > 0:
            if float(non_null.min()) < float(spec["min"]):
                domain_ok = False
                errors.append(f"Column '{col}' min {non_null.min()} < {spec['min']}")
        if "max" in spec and len(non_null) > 0:
            if float(non_null.max()) > float(spec["max"]):
                domain_ok = False
                errors.append(f"Column '{col}' max {non_null.max()} > {spec['max']}")
        if "pattern" in spec and len(non_null) > 0:
            pat = re.compile(spec["pattern"])
            bad = int((~non_null.astype(str).str.match(pat)).sum())
            if bad > 0:
                domain_ok = False
                errors.append(f"Column '{col}' has {bad} values failing pattern {spec['pattern']}")

    checks["null_checks"] = null_ok
    checks["domain_validation"] = domain_ok

    # 4. Outlier Diagnostics (IQR diagnostics logged; non-fatal unless extreme NaN/Inf)
    outlier_counts: Dict[str, int] = {}
    inf_found = False
    for col in df.select_dtypes(include=[np.number]).columns:
        vals = df[col].dropna().to_numpy(dtype=float)
        if np.isinf(vals).any():
            inf_found = True
            errors.append(f"Column '{col}' contains infinite values")
        if len(vals) >= 4:
            q1, q3 = np.percentile(vals, [25, 75])
            iqr = q3 - q1
            if iqr > 0:
                lower, upper = q1 - 3.0 * iqr, q3 + 3.0 * iqr
                outlier_counts[col] = int(((vals < lower) | (vals > upper)).sum())
            else:
                outlier_counts[col] = 0
    checks["outlier_diagnostics"] = not inf_found

    # 5. Privacy Checks (prohibited PII column names + regex scan on string columns)
    prohibited_cols = set(c.lower() for c in schema.get("prohibited_pii_columns", []))
    found_prohibited = [c for c in df.columns if c.lower() in prohibited_cols]
    pii_hits = 0
    for col in df.select_dtypes(include=["object", "string"]).columns:
        sample_vals = df[col].dropna().astype(str).head(1000)
        for pat in PII_PATTERNS:
            pii_hits += int(sample_vals.str.contains(pat, regex=True).sum())

    checks["privacy_checks"] = len(found_prohibited) == 0 and pii_hits == 0
    if found_prohibited:
        errors.append(f"Prohibited PII columns present: {found_prohibited}")
    if pii_hits > 0:
        errors.append(f"Detected {pii_hits} potential PII pattern matches in string columns")

    # 6. Provenance & Dataset Version Validation
    prov_ok = True
    version_ok = True
    if manifest is not None:
        if not manifest.get("is_synthetic", False):
            prov_ok = False
            errors.append("Manifest must explicitly mark is_synthetic: true for synthetic datasets")
        prov = manifest.get("provenance", {})
        for req_key in ("created_utc", "sha256", "licence"):
            if not prov.get(req_key):
                prov_ok = False
                errors.append(f"Manifest provenance missing required field: {req_key}")
        if csv_path is not None and csv_path.exists() and prov.get("sha256"):
            actual_sha = compute_sha256(csv_path)
            if actual_sha != prov["sha256"]:
                prov_ok = False
                errors.append("CSV SHA-256 checksum does not match manifest provenance")
        expected_ver = schema.get("dataset_version")
        actual_ver = manifest.get("dataset_version")
        if expected_ver and actual_ver != expected_ver:
            version_ok = False
            errors.append(f"Dataset version mismatch: manifest={actual_ver}, schema={expected_ver}")
    else:
        prov_ok = False
        version_ok = False
        errors.append("Manifest is required for provenance and version validation")

    checks["provenance_validation"] = prov_ok
    checks["version_validation"] = version_ok

    passed = all(checks.values()) and len(errors) == 0
    return ValidationReport(
        passed=passed,
        checks=checks,
        errors=errors,
        warnings=warnings,
        metrics={
            "row_count": int(len(df)),
            "column_count": int(len(df.columns)),
            "null_rates": null_rates,
            "extreme_outlier_counts_3iqr": outlier_counts,
        },
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate JDCL synthetic dataset.")
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--schema", type=Path, required=True)
    args = parser.parse_args()

    df = pd.read_csv(args.data)
    schema = load_yaml(args.schema)
    manifest = load_manifest(args.manifest)
    report = validate_dataset(df, schema=schema, manifest=manifest, csv_path=args.data)

    for k, v in report.checks.items():
        print(f"  [{'PASS' if v else 'FAIL'}] {k}")
    if report.errors:
        print("Errors:")
        for e in report.errors:
            print(f"  - {e}")
    sys.exit(0 if report.passed else 1)


if __name__ == "__main__":
    main()

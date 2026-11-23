"""Tests for schema compliance, duplicate detection, provenance, and privacy checks."""

import unittest

import pandas as pd

from jdcl.config import PROJECT_ROOT, load_yaml
from jdcl.data.generator import generate_jflm_2027_dataframe
from jdcl.data.manifest import load_manifest
from jdcl.quality.validator import validate_dataset


class TestDataQuality(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema = load_yaml(PROJECT_ROOT / "data" / "schemas" / "jflm_2027_schema.yml")
        cls.manifest = load_manifest(PROJECT_ROOT / "data" / "manifests" / "jflm_2027.yml")
        cls.csv_path = PROJECT_ROOT / "data" / "synthetic" / "jflm_2027.csv"
        cls.df = pd.read_csv(cls.csv_path)

    def test_production_synthetic_dataset_passes_all_checks(self) -> None:
        report = validate_dataset(self.df, self.schema, self.manifest, self.csv_path)
        self.assertTrue(report.passed, msg=f"Validation errors: {report.errors}")
        self.assertEqual(len(self.df), 10000)

    def test_duplicate_detection_fails_on_duplicate_pk(self) -> None:
        bad_df = pd.concat([self.df.head(5), self.df.head(1)], ignore_index=True)
        report = validate_dataset(bad_df, self.schema, self.manifest)
        self.assertFalse(report.passed)
        self.assertFalse(report.checks["duplicate_detection"])

    def test_privacy_check_fails_on_prohibited_pii_column(self) -> None:
        bad_df = generate_jflm_2027_dataframe(n_rows=50, seed=42)
        bad_df["nik"] = "3175010101900001"
        report = validate_dataset(bad_df, self.schema, self.manifest)
        self.assertFalse(report.passed)
        self.assertFalse(report.checks["privacy_checks"])

    def test_provenance_fails_when_manifest_missing(self) -> None:
        report = validate_dataset(self.df.head(20), self.schema, manifest=None)
        self.assertFalse(report.passed)
        self.assertFalse(report.checks["provenance_validation"])


if __name__ == "__main__":
    unittest.main()

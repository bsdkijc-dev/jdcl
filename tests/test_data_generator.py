"""Tests for deterministic synthetic data generation and reproducibility."""

import tempfile
import unittest
from pathlib import Path

from jdcl.data.generator import generate_and_save, generate_jflm_2027_dataframe


class TestDataGenerator(unittest.TestCase):
    def test_row_count_and_reproducibility(self) -> None:
        df1 = generate_jflm_2027_dataframe(n_rows=500, seed=12345)
        df2 = generate_jflm_2027_dataframe(n_rows=500, seed=12345)
        self.assertEqual(len(df1), 500)
        self.assertTrue(df1.equals(df2))

    def test_different_seeds_differ(self) -> None:
        df1 = generate_jflm_2027_dataframe(n_rows=200, seed=111)
        df2 = generate_jflm_2027_dataframe(n_rows=200, seed=222)
        self.assertFalse(df1["resolution_days"].equals(df2["resolution_days"]))

    def test_generate_and_save_creates_manifest_and_csv(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            csv_p = Path(tmp) / "test.csv"
            man_p = Path(tmp) / "test.yml"
            df, manifest = generate_and_save(n_rows=100, seed=99, csv_path=csv_p, manifest_path=man_p)
            self.assertTrue(csv_p.exists())
            self.assertTrue(man_p.exists())
            self.assertEqual(len(df), 100)
            self.assertTrue(manifest["is_synthetic"])
            self.assertFalse(manifest["provenance"]["human_publication_approval"])


if __name__ == "__main__":
    unittest.main()

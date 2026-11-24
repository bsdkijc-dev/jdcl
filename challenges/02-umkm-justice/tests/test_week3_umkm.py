import csv
import importlib.util
import pathlib
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]

GEN_SPEC = importlib.util.spec_from_file_location("gen_umkm", ROOT / "scripts" / "generate_umkm_pilot_sample.py")
gen_mod = importlib.util.module_from_spec(GEN_SPEC)
GEN_SPEC.loader.exec_module(gen_mod)

RUN_SPEC = importlib.util.spec_from_file_location("run_umkm", ROOT / "baseline" / "run_umkm_analysis.py")
run_mod = importlib.util.module_from_spec(RUN_SPEC)
RUN_SPEC.loader.exec_module(run_mod)


class TestWeek3UMKM(unittest.TestCase):
    def test_zero_imputation_and_pure_numeric_csv(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_dir = pathlib.Path(tmp)
            info = gen_mod.generate_umkm_pilot(tmp_dir)
            self.assertEqual(info["rows"], 60)
            self.assertEqual(info["missing_dispute_days"], 12)

            in_csv = tmp_dir / "umkm_justice_pilot.csv"
            with in_csv.open("r", encoding="utf-8") as f:
                raw_text = f.read()
                self.assertNotIn("Rp", raw_text)

            out_csv = tmp_dir / "summary.csv"
            res = run_mod.run_analysis(in_csv, out_csv)
            self.assertEqual(res["provinces"], 5)
            self.assertEqual(res["complete_dispute_rows"], 48)
            with out_csv.open("r", encoding="utf-8") as f:
                summary_rows = list(csv.DictReader(f))
            self.assertEqual(len(summary_rows), 5)


if __name__ == "__main__":
    unittest.main()

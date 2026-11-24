import importlib.util
import pathlib
import unittest

MOD_PATH = pathlib.Path(__file__).resolve().parents[1] / "baseline" / "umkm_baseline.py"
spec = importlib.util.spec_from_file_location("umkm_baseline", MOD_PATH)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class TestUMKMScaffold(unittest.TestCase):
    def test_zero_imputation_completeness(self):
        rows = [{"survival_rate": 0.82}, {"survival_rate": None}, {"survival_rate": ""}]
        self.assertEqual(mod.compute_completeness_rate(rows, "survival_rate"), 0.3333)
        self.assertEqual(mod.compute_completeness_rate([], "survival_rate"), 0.0)


if __name__ == "__main__":
    unittest.main()

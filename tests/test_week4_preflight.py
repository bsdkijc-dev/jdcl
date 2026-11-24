import importlib.util
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
MOD_PATH = ROOT / "scripts" / "preflight_audit.py"
spec = importlib.util.spec_from_file_location("preflight_audit", MOD_PATH)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class TestWeek4Preflight(unittest.TestCase):
    def test_preflight_audit_passes_all_challenges(self):
        summary = mod.run_audit(ROOT)
        self.assertTrue(summary["all_passed"], f"Preflight failed: {summary}")
        self.assertEqual(len(summary["results"]), 3)


if __name__ == "__main__":
    unittest.main()

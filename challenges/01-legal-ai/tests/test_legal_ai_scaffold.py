import importlib.util
import pathlib
import unittest

MOD_PATH = pathlib.Path(__file__).resolve().parents[1] / "baseline" / "evaluate_citations.py"
spec = importlib.util.spec_from_file_location("evaluate_citations", MOD_PATH)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class TestLegalAIScaffold(unittest.TestCase):
    def test_symbolic_gate_abstains_unverified(self):
        self.assertEqual(mod.symbolic_gate_check("PERMA", False), "ABSTAIN_UNVERIFIED")
        self.assertEqual(mod.symbolic_gate_check("UNKNOWN", True), "ABSTAIN_UNVERIFIED")
        self.assertEqual(mod.symbolic_gate_check("PERMA", True), "VERIFIED_RANK_3")

    def test_score_predictions(self):
        gt = {"q1": "PERMA_2012_02", "q2": "ABSTAIN_UNVERIFIED"}
        pred = {"q1": "PERMA_2012_02", "q2": "ABSTAIN_UNVERIFIED"}
        res = mod.score_predictions(gt, pred)
        self.assertEqual(res["exact_match"], 1.0)
        self.assertEqual(res["trap_abstention_accuracy"], 1.0)


if __name__ == "__main__":
    unittest.main()

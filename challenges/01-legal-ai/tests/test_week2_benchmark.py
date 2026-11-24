import csv
import importlib.util
import pathlib
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]

GEN_PATH = ROOT / "scripts" / "generate_legal_ai_benchmark.py"
gen_spec = importlib.util.spec_from_file_location("generate_legal_ai_benchmark", GEN_PATH)
gen_mod = importlib.util.module_from_spec(gen_spec)
gen_spec.loader.exec_module(gen_mod)

RUN_PATH = ROOT / "baseline" / "run_baseline.py"
run_spec = importlib.util.spec_from_file_location("run_baseline", RUN_PATH)
run_mod = importlib.util.module_from_spec(run_spec)
run_spec.loader.exec_module(run_mod)


class TestWeek2Benchmark(unittest.TestCase):
    def test_deterministic_generation_and_baseline(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_dir = pathlib.Path(tmp)
            summary = gen_mod.generate_benchmark(tmp_dir)
            self.assertEqual(summary["total_queries"], 1000)
            self.assertEqual(summary["verified_queries"], 750)
            self.assertEqual(summary["trap_queries"], 250)

            with (tmp_dir / "benchmark_queries.csv").open("r", encoding="utf-8") as f:
                rows = list(csv.DictReader(f))
            self.assertEqual(len(rows), 1000)

            sub_path = tmp_dir / "submission.csv"
            metrics = run_mod.run_pipeline(tmp_dir, sub_path)
            self.assertGreaterEqual(metrics["exact_match"], 0.70)
            self.assertEqual(metrics["trap_abstention_accuracy"], 1.0)


if __name__ == "__main__":
    unittest.main()

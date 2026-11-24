import csv
import importlib.util
import json
import pathlib
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]

GEN_SPEC = importlib.util.spec_from_file_location("gen_meta", ROOT / "scripts" / "generate_metadata_sample.py")
gen_mod = importlib.util.module_from_spec(GEN_SPEC)
GEN_SPEC.loader.exec_module(gen_mod)

IDX_SPEC = importlib.util.spec_from_file_location("build_idx", ROOT / "baseline" / "build_static_search_index.py")
idx_mod = importlib.util.module_from_spec(IDX_SPEC)
IDX_SPEC.loader.exec_module(idx_mod)


class TestWeek3Metadata(unittest.TestCase):
    def test_completeness_audit_and_static_index(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_dir = pathlib.Path(tmp)
            info = gen_mod.generate_metadata_sample(tmp_dir)
            self.assertEqual(info["courts"], 80)
            self.assertEqual(info["pending_verification"], 20)

            audit_csv = tmp_dir / "completeness_audit.csv"
            index_json = tmp_dir / "static_search_index.json"
            res = idx_mod.build_index(tmp_dir / "satker_registry_sample.csv", audit_csv, index_json)
            self.assertEqual(res["branches"], 4)
            self.assertEqual(res["indexed_courts"], 80)

            payload = json.loads(index_json.read_text(encoding="utf-8"))
            self.assertEqual(payload["count"], 80)
            with audit_csv.open("r", encoding="utf-8") as f:
                rows = list(csv.DictReader(f))
            self.assertEqual(len(rows), 4)


if __name__ == "__main__":
    unittest.main()

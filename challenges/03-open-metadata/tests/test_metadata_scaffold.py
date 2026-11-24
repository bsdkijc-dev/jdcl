import importlib.util
import pathlib
import unittest

MOD_PATH = pathlib.Path(__file__).resolve().parents[1] / "baseline" / "validate_metadata.py"
spec = importlib.util.spec_from_file_location("validate_metadata", MOD_PATH)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class TestMetadataScaffold(unittest.TestCase):
    def test_validate_satker_row(self):
        complete = {
            "satker_id": "MA-COURT-001",
            "court_name": "PN Mataram",
            "province_code": "52",
            "verification_status": "VERIFIED",
        }
        self.assertEqual(mod.validate_satker_row(complete), [])
        incomplete = {"satker_id": "MA-COURT-002", "court_name": ""}
        self.assertEqual(
            mod.validate_satker_row(incomplete),
            ["court_name", "province_code", "verification_status"],
        )


if __name__ == "__main__":
    unittest.main()

import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
CHALLENGES = [
    ROOT / "challenges" / "01-legal-ai",
    ROOT / "challenges" / "02-umkm-justice",
    ROOT / "challenges" / "03-open-metadata",
]
REQUIRED_SECTIONS = [
    "## 1. Public Problem",
    "## 2. Research Question",
    "## 3. Measurable Objective",
    "## 4. Verified & Synthetic Dataset",
    "## 5. Reproducible Methodology",
    "## 6. Participant Instructions",
    "## 7. Evaluation Criteria",
    "## 8. Submission Requirements",
    "## 9. Ethical & Privacy Safeguards",
    "## 10. Open-Source Output Strategy",
]


class TestGovernanceAndMetadata(unittest.TestCase):
    def test_governance_docs_exist(self):
        self.assertTrue((ROOT / "CONTRIBUTING.md").is_file())
        self.assertTrue((ROOT / "ETHICS_AND_PRIVACY.md").is_file())
        self.assertTrue((ROOT / ".github" / "workflows" / "jdcl-challenges-ci.yml").is_file())

    def test_challenge_framework_sections_and_kaggle_metadata(self):
        for ch in CHALLENGES:
            readme = (ch / "README.md").read_text(encoding="utf-8")
            for sec in REQUIRED_SECTIONS:
                self.assertIn(sec, readme, f"Missing {sec} in {ch.name}")
            self.assertTrue((ch / "RULES.md").is_file(), f"Missing RULES.md in {ch.name}")
            meta_path = ch / "kaggle" / "dataset-metadata.json"
            self.assertTrue(meta_path.is_file(), f"Missing dataset-metadata.json in {ch.name}")
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
            self.assertTrue(6 <= len(meta["title"]) <= 50, f"Invalid title length in {ch.name}")
            self.assertTrue(20 <= len(meta["subtitle"]) <= 80, f"Invalid subtitle length in {ch.name}")


if __name__ == "__main__":
    unittest.main()

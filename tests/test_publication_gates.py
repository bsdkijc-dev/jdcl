"""Tests enforcing publication restrictions and human approval gates."""

import unittest

from jdcl.config import PROJECT_ROOT, get_settings, load_yaml


class TestPublicationGates(unittest.TestCase):
    def test_external_publishing_disabled_by_default(self) -> None:
        settings = get_settings()
        gov = settings["governance"]
        self.assertFalse(gov["allow_external_publish"])
        self.assertFalse(gov["allow_kaggle_activation"])
        self.assertFalse(gov["allow_real_judicial_records"])
        self.assertTrue(gov["require_human_approval_for_release"])

    def test_competition_registry_requires_human_approval(self) -> None:
        reg = load_yaml(PROJECT_ROOT / "config" / "competition_registry.yml")
        comp = reg["competitions"][0]
        self.assertEqual(comp["cost_tier"], "FREE_COMMUNITY_ONLY")
        self.assertEqual(comp["status"], "DRAFT_LOCAL_ONLY")
        self.assertTrue(comp["human_approval_required"])


if __name__ == "__main__":
    unittest.main()

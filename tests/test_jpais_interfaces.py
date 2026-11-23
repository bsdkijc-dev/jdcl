"""Tests for offline-capable JPAIS interfaces."""

import tempfile
import unittest
from pathlib import Path

from jdcl.jpais.interfaces import ExperimentRecord, ProvenanceRecord, PublicationApprovalRecord
from jdcl.jpais.local_store import LocalJPAISStore


class TestJPAISInterfaces(unittest.TestCase):
    def test_offline_store_roundtrip_and_approval_gate(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            store = LocalJPAISStore(store_dir=Path(tmp))
            prov = store.register_provenance(
                ProvenanceRecord(
                    dataset_id="jflm_2027_synthetic_v1",
                    version="1.0.0-synthetic",
                    sha256="abc123",
                    is_synthetic=True,
                    classification="P1_SYNTHETIC_PUBLIC_CANDIDATE",
                    created_utc="2026-11-23T08:00:00Z",
                )
            )
            self.assertEqual(prov["mode"], "offline_local")

            exp = store.track_experiment(
                ExperimentRecord(
                    experiment_id="exp_001",
                    model_name="RidgeLinearBaseline",
                    metrics={"mae": 10.5},
                    fairness={"max_mae_gap": 2.1},
                    seed=20270101,
                )
            )
            self.assertEqual(exp["model_name"], "RidgeLinearBaseline")

            # Publication approval must remain False even if requested with True
            store.request_publication_approval(
                PublicationApprovalRecord(
                    artifact_id="jflm_2027_synthetic_v1",
                    classification="P1_SYNTHETIC_PUBLIC_CANDIDATE",
                    technical_checks_passed=True,
                    human_approved=True,
                )
            )
            checked = store.check_publication_approval("jflm_2027_synthetic_v1")
            self.assertFalse(checked.human_approved)


if __name__ == "__main__":
    unittest.main()

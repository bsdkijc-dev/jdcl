"""Offline-first local JSON store implementing JPAISAdapter without any live API."""

from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

from jdcl.config import PROJECT_ROOT
from jdcl.jpais.interfaces import (
    ExperimentRecord,
    ProvenanceRecord,
    PublicationApprovalRecord,
)


class LocalJPAISStore:
    """Zero-cost local file-backed JPAIS store (no network, no credentials)."""

    def __init__(self, store_dir: Path | None = None) -> None:
        self.store_dir = store_dir or (PROJECT_ROOT / "artifacts" / "jpais_store")
        self.store_dir.mkdir(parents=True, exist_ok=True)

    def _write_json(self, category: str, item_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        cat_dir = self.store_dir / category
        cat_dir.mkdir(parents=True, exist_ok=True)
        safe_id = item_id.replace("/", "_")
        target = cat_dir / f"{safe_id}.json"
        enriched = {
            **payload,
            "recorded_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "mode": "offline_local",
        }
        with open(target, "w", encoding="utf-8") as f:
            json.dump(enriched, f, indent=2)
        return enriched

    def register_provenance(self, record: ProvenanceRecord) -> Dict[str, Any]:
        return self._write_json("provenance", record.dataset_id, asdict(record))

    def record_governance_status(self, dataset_id: str, checks: Dict[str, bool]) -> Dict[str, Any]:
        return self._write_json("governance", dataset_id, {"dataset_id": dataset_id, "checks": checks})

    def log_evaluation_metrics(self, run_id: str, metrics: Dict[str, float]) -> Dict[str, Any]:
        return self._write_json("metrics", run_id, {"run_id": run_id, "metrics": metrics})

    def register_benchmark(self, benchmark_id: str, details: Dict[str, Any]) -> Dict[str, Any]:
        return self._write_json("benchmarks", benchmark_id, {"benchmark_id": benchmark_id, **details})

    def track_experiment(self, experiment: ExperimentRecord) -> Dict[str, Any]:
        return self._write_json("experiments", experiment.experiment_id, asdict(experiment))

    def log_policy_evaluation(self, policy_id: str, evaluation: Dict[str, Any]) -> Dict[str, Any]:
        return self._write_json("policy_evals", policy_id, {"policy_id": policy_id, **evaluation})

    def request_publication_approval(self, record: PublicationApprovalRecord) -> Dict[str, Any]:
        # Hard guardrail: never auto-approve external publication
        payload = asdict(record)
        payload["human_approved"] = False
        return self._write_json("publication_approvals", record.artifact_id, payload)

    def check_publication_approval(self, artifact_id: str) -> PublicationApprovalRecord:
        target = self.store_dir / "publication_approvals" / f"{artifact_id.replace('/', '_')}.json"
        if not target.exists():
            return PublicationApprovalRecord(
                artifact_id=artifact_id,
                classification="P1_SYNTHETIC_PUBLIC_CANDIDATE",
                technical_checks_passed=False,
                human_approved=False,
            )
        with open(target, "r", encoding="utf-8") as f:
            data = json.load(f)
        return PublicationApprovalRecord(
            artifact_id=data["artifact_id"],
            classification=data["classification"],
            technical_checks_passed=bool(data["technical_checks_passed"]),
            human_approved=bool(data.get("human_approved", False)),
            approver_name=data.get("approver_name", ""),
            approval_timestamp_utc=data.get("approval_timestamp_utc", ""),
        )

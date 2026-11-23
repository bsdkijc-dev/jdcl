"""Abstract/protocol interfaces for JPAIS integration (no live API required)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Protocol


@dataclass
class ProvenanceRecord:
    dataset_id: str
    version: str
    sha256: str
    is_synthetic: bool
    classification: str
    created_utc: str


@dataclass
class ExperimentRecord:
    experiment_id: str
    model_name: str
    metrics: Dict[str, float]
    fairness: Dict[str, Any]
    seed: int
    notes: str = ""


@dataclass
class PublicationApprovalRecord:
    artifact_id: str
    classification: str
    technical_checks_passed: bool
    human_approved: bool = False
    approver_name: str = ""
    approval_timestamp_utc: str = ""


class JPAISAdapter(Protocol):
    """Modular interface for JPAIS governance, provenance, and research tracking."""

    def register_provenance(self, record: ProvenanceRecord) -> Dict[str, Any]: ...
    def record_governance_status(self, dataset_id: str, checks: Dict[str, bool]) -> Dict[str, Any]: ...
    def log_evaluation_metrics(self, run_id: str, metrics: Dict[str, float]) -> Dict[str, Any]: ...
    def register_benchmark(self, benchmark_id: str, details: Dict[str, Any]) -> Dict[str, Any]: ...
    def track_experiment(self, experiment: ExperimentRecord) -> Dict[str, Any]: ...
    def log_policy_evaluation(self, policy_id: str, evaluation: Dict[str, Any]) -> Dict[str, Any]: ...
    def check_publication_approval(self, artifact_id: str) -> PublicationApprovalRecord: ...
    def request_publication_approval(self, record: PublicationApprovalRecord) -> Dict[str, Any]: ...

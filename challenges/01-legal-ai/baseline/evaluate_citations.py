"""Deterministic baseline & scorer for Challenge 01: Legal AI Citation Verification."""

HIERARCHY_RANK = {"UU": 1, "PP": 2, "PERMA": 3, "SEMA": 4}


def score_predictions(ground_truth: dict[str, str], predictions: dict[str, str]) -> dict[str, float]:
    """Compute exact citation match accuracy and trap abstention accuracy."""
    if not ground_truth:
        raise ValueError("ground_truth must not be empty")
    total = len(ground_truth)
    correct = 0
    trap_total = 0
    trap_correct = 0
    for qid, expected in ground_truth.items():
        pred = predictions.get(qid, "")
        if pred == expected:
            correct += 1
        if expected == "ABSTAIN_UNVERIFIED":
            trap_total += 1
            if pred == "ABSTAIN_UNVERIFIED":
                trap_correct += 1
    return {
        "exact_match": round(correct / total, 4),
        "trap_abstention_accuracy": round(trap_correct / trap_total, 4) if trap_total else 1.0,
    }


def symbolic_gate_check(doc_type: str, is_verified: bool) -> str:
    """Enforce statutory hierarchy and verification gate before citation emission."""
    if not is_verified or doc_type not in HIERARCHY_RANK:
        return "ABSTAIN_UNVERIFIED"
    return f"VERIFIED_RANK_{HIERARCHY_RANK[doc_type]}"

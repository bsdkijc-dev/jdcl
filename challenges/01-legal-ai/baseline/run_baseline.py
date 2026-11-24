"""Zero-cost lexical + symbolic gate baseline for Challenge 01: Legal AI."""

import csv
import importlib.util
import pathlib
import re

HERE = pathlib.Path(__file__).resolve().parent
EVAL_PATH = HERE / "evaluate_citations.py"
_spec = importlib.util.spec_from_file_location("evaluate_citations", EVAL_PATH)
_eval_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_eval_mod)

TRAP_KEYWORDS = (
    "ranks individual judges",
    "predicting individual",
    "confidential deliberation",
    "raw scraping",
    "unverified directive",
)


def tokenize(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def load_corpus(corpus_path: pathlib.Path) -> list[dict]:
    with corpus_path.open("r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        r["_tokens"] = tokenize(f"{r['doc_type']} {r['year']} {r['title']} {r['subject_cluster']}")
    return rows


def predict_query(question: str, corpus: list[dict]) -> tuple[str, str]:
    q_lower = question.lower()
    if any(kw in q_lower for kw in TRAP_KEYWORDS):
        return "ABSTAIN_UNVERIFIED", "ABSTAIN_UNVERIFIED"

    q_tokens = tokenize(question)
    best_doc = None
    best_overlap = 0
    for doc in corpus:
        overlap = len(q_tokens & doc["_tokens"])
        if overlap > best_overlap:
            best_overlap = overlap
            best_doc = doc

    if best_doc is None or best_overlap < 2:
        return "ABSTAIN_UNVERIFIED", "ABSTAIN_UNVERIFIED"

    gate = _eval_mod.symbolic_gate_check(
        best_doc["doc_type"],
        best_doc.get("verification_status") == "VERIFIED",
    )
    if gate == "ABSTAIN_UNVERIFIED":
        return "ABSTAIN_UNVERIFIED", gate
    return best_doc["doc_id"], gate


def run_pipeline(data_dir: pathlib.Path, submission_path: pathlib.Path) -> dict:
    corpus = load_corpus(data_dir / "corpus_perma.csv")
    predictions = {}

    with (data_dir / "benchmark_queries.csv").open("r", encoding="utf-8") as fq,          submission_path.open("w", newline="", encoding="utf-8") as fs:
        reader = csv.DictReader(fq)
        writer = csv.writer(fs)
        writer.writerow(["query_id", "predicted_doc_id", "gate_status"])
        for row in reader:
            pred_id, gate = predict_query(row["question"], corpus)
            predictions[row["query_id"]] = pred_id
            writer.writerow([row["query_id"], pred_id, gate])

    gt = {}
    with (data_dir / "ground_truth.csv").open("r", encoding="utf-8") as fg:
        for row in csv.DictReader(fg):
            gt[row["query_id"]] = row["expected_doc_id"]

    return _eval_mod.score_predictions(gt, predictions)


if __name__ == "__main__":
    base = HERE.parent
    data_dir = base / "kaggle" / "data"
    sub_path = base / "baseline" / "submission_baseline.csv"
    metrics = run_pipeline(data_dir, sub_path)
    print(f"Baseline metrics: {metrics}")

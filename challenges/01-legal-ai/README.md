# Challenge 01 — Indonesian Legal AI Retrieval & Citation Verification (Project 03)

## 1. Public Problem
Generative AI systems frequently fabricate Indonesian legal citations. Reliable public-interest legal information tools require deterministic verification against authoritative statutory and regulatory hierarchies.

## 2. Research Question
How accurately can open-source AI retrieval systems ground answers in verified Indonesian legal sources (PERMA and statutory hierarchy) while abstaining on unverified or trap citations?

## 3. Measurable Objective
Maximize Citation Verification Macro F1, Retrieval Recall@5, and Hallucination Abstention Accuracy (`ABSTAIN_UNVERIFIED`) at zero API cost.

## 4. Verified & Synthetic Dataset
- **Verified Corpus:** Public `judicialcollege/perma-master-registry` (107 PERMA, 1980–2025) and MA Integration `p05_approved_legal_knowledge_index.json` (11 verified provisions).
- **Synthetic Benchmark:** 1,000 deterministic synthetic Q&A pairs including adversarial trap citations (staged Private pending human launch approval).

## 5. Reproducible Methodology
Deterministic symbolic hierarchy gate (`UU -> PP -> PERMA -> SEMA`) paired with open-source lexical/BM25 retrieval baseline in `baseline/evaluate_citations.py`.

## 6. Participant Instructions
1. Fork `bsdkijc-dev/jdcl` and inspect `challenges/01-legal-ai/baseline/evaluate_citations.py`.
2. Generate `submission.csv` mapping `query_id` to `verified_doc_id` or `ABSTAIN_UNVERIFIED`.
3. Run `python3 -m unittest discover -s challenges/01-legal-ai/tests`.

## 7. Evaluation Criteria
- Citation Verification Macro F1: 50%
- Retrieval Recall@5: 30%
- Abstention Accuracy on Trap Citations: 20%

## 8. Submission Requirements
`submission.csv`, open-source inference script, and model card confirming zero paid APIs.

## 9. Ethical & Privacy Safeguards
Regulatory texts only; zero litigant or judge PII; predicting individual case outcomes or ranking judges is strictly prohibited.

## 10. Open-Source Output Strategy
MIT/Apache-2.0 evaluation harness and benchmark published under `bsdkijc-dev/jdcl` upon human approval.

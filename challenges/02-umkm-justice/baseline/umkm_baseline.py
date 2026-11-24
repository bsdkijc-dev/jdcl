"""Zero-imputation completeness & aggregation baseline for Challenge 02: UMKM Justice."""


def compute_completeness_rate(records: list[dict], field: str) -> float:
    """Return fraction of records with non-empty values for `field` (zero imputation)."""
    if not records:
        return 0.0
    present = sum(1 for r in records if r.get(field) not in (None, "", "NULL"))
    return round(present / len(records), 4)

"""Schema completeness validator baseline for Challenge 03: Open Judicial Metadata."""

REQUIRED_SATKER_FIELDS = ("satker_id", "court_name", "province_code", "verification_status")


def validate_satker_row(row: dict) -> list[str]:
    """Return list of missing required fields for a court satker record."""
    return [f for f in REQUIRED_SATKER_FIELDS if row.get(f) in (None, "", "NULL")]

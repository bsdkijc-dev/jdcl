"""Competition registry loader."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

from jdcl.config import PROJECT_ROOT, load_yaml


def load_competition_registry(path: Path | None = None) -> Dict[str, Any]:
    target = path or (PROJECT_ROOT / "config" / "competition_registry.yml")
    return load_yaml(target)


def get_competition_metadata(competition_id: str = "jflm-2027") -> Dict[str, Any]:
    reg = load_competition_registry()
    for comp in reg.get("competitions", []):
        if comp.get("competition_id") == competition_id:
            return comp
    raise KeyError(f"Competition '{competition_id}' not found in registry")

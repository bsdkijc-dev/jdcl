"""Configuration loader for JDCL v1.0."""

from pathlib import Path
from typing import Any, Dict
import yaml


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def load_yaml(path: Path) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def get_settings(settings_path: Path | None = None) -> Dict[str, Any]:
    target = settings_path or (PROJECT_ROOT / "config" / "settings.yml")
    return load_yaml(target)

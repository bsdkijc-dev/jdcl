#!/usr/bin/env bash
set -euo pipefail

# Stage JDCL Challenges 01-03 datasets to Kaggle as PRIVATE only (v1.0-ZC).
# Never passes --public; human approval is required before changing visibility.

KAGGLE_BIN="${KAGGLE_BIN:-$HOME/.kaggle-venv/bin/kaggle}"
if ! command -v "$KAGGLE_BIN" >/dev/null 2>&1; then
  KAGGLE_BIN="$(command -v kaggle || true)"
fi

if [ -z "$KAGGLE_BIN" ]; then
  echo "ERROR: kaggle CLI not found. Install in ~/.kaggle-venv or set KAGGLE_BIN."
  exit 1
fi

python3 scripts/preflight_audit.py

for ch in 01-legal-ai 02-umkm-justice 03-open-metadata; do
  echo "Staging Private Kaggle dataset for challenges/$ch..."
  "$KAGGLE_BIN" datasets create -p "challenges/$ch/kaggle" -r zip
done

echo "Done. All datasets staged as PRIVATE pending human review."

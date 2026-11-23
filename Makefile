.PHONY: help setup generate validate test notebooks dashboard clean

PYTHON ?= python3
PYTHONPATH := src

help:
	@echo "JDCL v1.0 — Justice Delivery Competition Lab (Zero-Cost Community Mandate)"
	@echo "  make generate   - Generate deterministic 10,000-row synthetic JFLM 2027 dataset & manifest"
	@echo "  make validate   - Run data quality, schema, provenance, and privacy validation"
	@echo "  make test       - Run full automated test suite"
	@echo "  make dashboard  - Launch local Streamlit research dashboard"
	@echo "  make clean      - Remove Python caches"

generate:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m jdcl.data.generator --rows 10000 --seed 20270101

validate:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m jdcl.quality.validator --data data/synthetic/jflm_2027.csv --manifest data/manifests/jflm_2027.yml --schema data/schemas/jflm_2027_schema.yml

test:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m unittest discover -s tests -p "test_*.py" -v

dashboard:
	PYTHONPATH=$(PYTHONPATH) streamlit run app/dashboard.py --server.address 127.0.0.1

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

.PHONY: install test lint pipeline clean

install:
	pip install -e ".[dev]"

test:
	pytest -q

lint:
	ruff check .

# Full demo pipeline on the data shipped in the repo.
pipeline:
	python scripts/run_preprocess.py
	python scripts/run_eda.py
	python scripts/run_forecast.py

clean:
	rm -rf docs/*.png src/*.egg-info .pytest_cache __pycache__

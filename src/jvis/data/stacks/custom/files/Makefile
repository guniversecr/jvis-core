.PHONY: run test lint

run:
	python -m src.main

test:
	python -m pytest tests/ -v

lint:
	python -m ruff check src/ tests/

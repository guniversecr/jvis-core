.PHONY: install test lint format audit typecheck verify generate clean bump-patch bump-minor bump-major sync-public

PYTHON := .venv/bin/python3

install:
	$(PYTHON) -m pip install -e ".[test]"

test:
	$(PYTHON) -m pytest tests/ -v

lint:
	.venv/bin/ruff check src/ tests/
	.venv/bin/ruff format --check src/ tests/

format:
	.venv/bin/ruff format src/ tests/

audit:
	.venv/bin/ruff check src/ tests/
	$(PYTHON) -m bandit -r src/ -c pyproject.toml -q
	.venv/bin/pip-audit

typecheck:
	$(PYTHON) -m mypy src/ --strict

verify: lint audit typecheck test
	@echo "All checks passed."

generate:
	$(PYTHON) .jvis/agent-engine/engine.py generate-all --platform all

bump-patch:
	$(PYTHON) -m jvis bump patch

bump-minor:
	$(PYTHON) -m jvis bump minor

bump-major:
	$(PYTHON) -m jvis bump major

sync-public:
	$(PYTHON) scripts/sync_to_public.py $(PUBLIC_REPO_PATH)

clean:
	rm -rf dist/ build/ *.egg-info src/jvis/data/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true

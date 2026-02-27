# src/jvis/ — CLI Source Module

1. **Data-driven stacks** — Stack behavior comes from `data/stacks/*/manifest.yaml`, not Python code. Never add stack-specific Python logic.
2. **Module structure** — `cli.py` (Click commands) → `scaffold/` (generation) → `data/` (manifests + templates). Keep layers separate.
3. **Imports** — Use `from jvis.scaffold.stack_runner import run_stack`, not relative imports. All public functions need type annotations.
4. **Version guard** — `__main__.py` and `cli.py` check Python 3.12+ before any `from jvis import ...` to avoid SyntaxError on older versions.

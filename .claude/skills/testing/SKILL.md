# Testing Skill

Knowledge for writing and running tests in the JVIS framework.

## Test Structure

```
tests/
├── conftest.py           # Shared fixtures (tmp_path factories, stack helpers)
├── fixtures/             # Test data files
├── unit/                 # Fast, isolated tests
│   ├── test_scaffold.py  # Stack scaffold generation tests
│   ├── test_cli.py       # CLI command tests
│   ├── test_detection.py # Project state detection tests
│   └── test_validation.py # Input validation tests
├── integration/          # Cross-module tests
│   └── test_functional_scaffolds.py  # Cross-stack scaffold validation
└── smoke/                # End-to-end smoke tests
```

## Running Tests

```bash
make test                          # All tests verbose
python3 -m pytest tests/ -v       # Same thing
python3 -m pytest tests/unit/ -x  # Unit only, stop on first failure
python3 -m pytest -k "fastapi"    # Filter by name
```

## Key Fixtures (`conftest.py`)

- `tmp_path` — pytest built-in, creates temp directory per test
- Stack generation helpers use `tmp_path` + `run_stack()` to generate and inspect output

## Scaffold Testing Pattern

For every functional stack, test that:

1. **`run_stack()` succeeds** — generates all files without errors
2. **No Jinja2 artifacts** — scan all generated files for `{{` or `{%`
3. **Expected structure** — verify key files exist (entities, controllers, tests)
4. **Content correctness** — check specific strings exist in generated files

Example from `test_scaffold.py`:

```python
def test_python_fastapi_functional_scaffold(self, tmp_path):
    run_stack("python-fastapi", tmp_path / "test-project", context)
    # Verify files exist
    assert (tmp_path / "test-project" / "src" / "domain" / "entities").is_dir()
    # Verify content
    content = (tmp_path / "test-project" / "src" / "main.py").read_text()
    assert "items" in content
```

## Parametrize for Multi-Stack

Use `@pytest.mark.parametrize` for tests that apply to all stacks:

```python
@pytest.mark.parametrize("stack_id", ["python-fastapi", "nodejs-express", "react-vite"])
def test_no_jinja2_artifacts(self, stack_id, tmp_path):
    # Generates and scans each stack
```

## In-Memory Database for Tests

- **Python (SQLAlchemy):** `sqlite+aiosqlite://` with `StaticPool`
- **Node.js (Prisma):** Test files use mock repositories (no real DB)
- **React:** No database (frontend tests use mocked API responses)

**CRITICAL:** Never connect to real databases in tests. Use mocks or in-memory alternatives.

## Integration Test Structure

`tests/integration/test_functional_scaffolds.py` — Cross-stack validation:

- `TestFunctionalStackGeneration` — Parameterized generation across stacks
- `TestJinja2ArtifactDetection` — Scan for template artifacts
- `TestItemEntityConsistency` — Verify `name` + `description` fields across stacks
- `TestDatabaseConditionals` — Verify DB driver matches selected database type

## Test Counts

Current baseline: **443 tests** (all passing). Any new feature should maintain or increase this count.

## Pre-Commit Testing

Before committing: `python3 -m pytest tests/ -v` — ALL tests must pass. Never commit with failing tests.

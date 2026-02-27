# Python Patterns Skill

Knowledge for Python development within the JVIS framework.

## Python Requirements

- **Python 3.12+** (runtime check in `__main__.py` and `cli.py`)
- **pyproject.toml** only (no setup.py, no requirements.txt for core deps)
- Build system: Hatchling

## Tooling

### Ruff (Linting + Formatting)

Config lives in `pyproject.toml` under `[tool.ruff]`:
- `target-version = "py312"`
- `line-length = 120`
- Select rules: E, F, I, N, W, UP, B, C4, SIM, RUF

Commands:
- `ruff check src/ tests/` — lint
- `ruff format src/ tests/` — format
- `ruff check --fix src/` — auto-fix

### MyPy (Type Checking)

- `python3 -m mypy src/ --strict`
- All public functions must have type annotations
- Use `from __future__ import annotations` for forward references

### Bandit (Security)

- `python3 -m bandit -r src/ -c pyproject.toml -q`
- Config in `[tool.bandit]` section of pyproject.toml if present

## Clean Architecture Layers

JVIS Python projects follow Clean Architecture (inside-out dependency):

```
domain/          # Pure Python: entities, interfaces, errors (no framework deps)
  entities/      # Dataclasses or Pydantic models
  interfaces/    # Abstract base classes (ABCs)
  errors/        # Custom exception hierarchy

use_cases/       # Business logic: services (depend on domain abstractions)
  item_service.py

infrastructure/  # External concerns: DB, config, repositories
  database/      # SQLAlchemy engine, session factory
  repositories/  # Concrete implementations of domain interfaces
  config/        # Environment variable loading

controllers/     # HTTP layer: FastAPI routers (depend on use_cases)
  items.py       # Route handlers
```

**Dependency rule:** Domain has zero imports from other layers. Controllers depend on use_cases, which depend on domain interfaces. Infrastructure implements domain interfaces.

## Async SQLAlchemy Patterns

For `python-fastapi` stack templates:

```python
# Database session (infrastructure/database.py)
engine = create_async_engine(DATABASE_URL)
async_session = async_sessionmaker(engine, expire_on_commit=False)

# Repository pattern (infrastructure/repositories/)
class ItemRepository(IItemRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
```

### Test Database Pattern

Tests use in-memory SQLite with `StaticPool` + `dependency_overrides`:

```python
# conftest.py
engine = create_async_engine("sqlite+aiosqlite://", poolclass=StaticPool)
# Override FastAPI dependency injection for test session
```

See: `src/jvis/data/stacks/python-fastapi/files/` for reference templates

## Version Guard Pattern

Both CLI entry points validate Python version before importing JVIS modules:

```python
import sys
if sys.version_info < (3, 12):
    print(f"Error: JVIS requires Python 3.12+. Current: {sys.version_info.major}.{sys.version_info.minor}")
    sys.exit(1)
```

This runs **before** any `from jvis import ...` to avoid SyntaxError on older Python.

See: `docs/notes/lessons-learned.md` — "requires-python in pyproject.toml Is Not Enough"

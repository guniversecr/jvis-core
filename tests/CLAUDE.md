# tests/ — Test Suite Rules

1. **No production databases** — Use `sqlite+aiosqlite://` with `StaticPool` for Python, mock repositories for Node.js. Never connect to real databases.
2. **Scaffold test pattern** — Every stack test must: call `run_stack()`, verify no Jinja2 artifacts (`{{`, `{%`), check expected files exist.
3. **Naming** — `test_<stack>_<what>` for unit tests, `Test<Feature>` classes for integration. Use `@pytest.mark.parametrize` for multi-stack tests.
4. **Baseline** — All tests must pass. New features must maintain or increase test count. Run `make test` before committing. See `docs/STATUS.md` for current counts.

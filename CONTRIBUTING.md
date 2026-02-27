# Contributing to JVIS

Contributions are welcome. This guide covers the most useful ways to help.

## Setup

```bash
git clone https://github.com/guniversecr/jvis.git
cd jvis
pip install -e ".[test]"       # editable install with test deps
pip install pre-commit
pre-commit install              # install git hooks
make test                        # verify everything passes
```

Requires Python 3.12+ and Bash 4.0+.

## Pre-commit Hooks

This project uses pre-commit hooks to catch issues before they reach CI:

- **YAML/JSON validation** - catches syntax errors
- **Secret detection** - blocks commits with private keys or secrets
- **Ruff** - Python linting and formatting
- **Branch protection** - prevents direct commits to `main`

Hooks run automatically on `git commit`. To run manually:

```bash
pre-commit run --all-files
```

## Ways to Contribute

### Add an Agent

Agent configs live in `.jvis/agents/<pack>/<name>.yaml`. Follow the schema at `.jvis/agent-engine/schemas/agent.schema.yaml`.

1. Create `your-agent.yaml` with `name`, `persona`, `commands`, and `stack` fields
2. Run `python .jvis/agent-engine/engine.py generate your-agent --platform all` to generate output
3. Test the generated commands in Claude Code or Cursor
4. Submit a PR with the YAML config and generated output

### Improve a Stack

Stack scaffolding scripts are in `stacks/`. The goal is to make `jvis new --stack <name>` generate runnable code, not just empty directories.

### Add Platform Support

Platform templates are Jinja2 files in `.jvis/agent-engine/templates/`. Adding support for a new IDE means creating a new template (e.g., `windsurf.md`) and updating `engine.py` to support a `--platform windsurf` flag.

### Report Issues

File issues for:
- Agent workflows that break or produce bad results
- Template quality problems
- CLI errors or missing help text
- Documentation that contradicts reality

### Fix Bugs

Run `make test` to find existing failures. Check `tests/` for coverage gaps.

## Code Standards

- Python: Ruff for formatting/linting, type hints on all functions
- Tests: pytest, in `tests/unit/` or `tests/integration/`
- Commits: short imperative subject line, explain "why" in the body

## CI Security Checks

All PRs are automatically scanned by:
- **Bandit** - Python static analysis for security issues
- **TruffleHog** - secret detection in git history

These must pass before merging.

## Adding Dependencies

New dependencies require justification in the PR description. Keep the dependency footprint minimal -- JVIS's core install should remain lightweight (click, jinja2, pyyaml).

## Pull Request Process

1. Fork the repo, create a feature branch
2. Make your changes
3. Run `make lint test` and `pre-commit run --all-files`
4. Submit a PR against `main` with a clear description of what and why
5. Wait for CI checks (tests, Bandit, TruffleHog) to pass
6. Address review feedback from CODEOWNERS

## What Not to Do

- Don't add agents without testing them in a real workflow
- Don't add dependencies unless absolutely necessary
- Don't create features for hypothetical future needs

## License

By contributing, you agree that your contributions will be licensed under the Apache License 2.0.

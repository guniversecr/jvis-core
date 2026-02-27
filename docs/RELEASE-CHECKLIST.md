# Release Checklist — PyPI Publish

## Pre-requisites (one-time setup)

- [ ] **GitHub Environment: `testpypi`** — Create at Settings > Environments
  - Add trusted publisher in TestPyPI: owner=`guniversecr`, repo=`jvis`, workflow=`publish-pypi.yml`, environment=`testpypi`
- [ ] **GitHub Environment: `pypi`** — Create at Settings > Environments
  - Add trusted publisher in PyPI: owner=`guniversecr`, repo=`jvis`, workflow=`publish-pypi.yml`, environment=`pypi`
  - Add required reviewer (manual approval before PyPI publish)
- [ ] **Register `jvis` package name** — First TestPyPI publish claims it

## Before Every Release

### Quality Gate (minimum score: 8.5/10)

- [ ] All tests pass: `make test`
- [ ] E2E wheel tests pass: `JVIS_E2E=1 pytest tests/integration/test_wheel_install.py`
- [ ] Lint clean: `make lint`
- [ ] Type check clean: `make typecheck`
- [ ] Wheel builds without warnings: `python -m build --wheel`
- [ ] `jvis new` works from installed wheel (custom, fastapi, react-vite)
- [ ] `jvis add` works from installed wheel (creates .jvis/, .claude/, CLAUDE.md)
- [ ] Version synced in all 3 locations:
  - `pyproject.toml` → `version = "X.Y.Z"`
  - `.jvis/version` → `X.Y.Z`
  - `.jvis/VERSION.yaml` → `version: X.Y.Z`

### Version Bump

```bash
# Update all 3 files, then:
make test && make lint
git add pyproject.toml .jvis/version .jvis/VERSION.yaml
git commit -m "chore: bump version to X.Y.Z"
git push
```

## TestPyPI Dry-Run

```bash
# Via GitHub Actions (recommended)
# Go to Actions > "Publish to PyPI" > Run workflow > target: testpypi

# Verify installation
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ jvis
jvis --version
jvis new -n test-proj -s custom -p /tmp/test-proj -y
```

## PyPI Release

```bash
# Option A: Create GitHub release (triggers automatic publish)
gh release create vX.Y.Z --title "JVIS vX.Y.Z" --generate-notes

# Option B: Manual dispatch
# Go to Actions > "Publish to PyPI" > Run workflow > target: pypi
```

## Post-Release Verification

```bash
pip install jvis
jvis --version
jvis new -n verify-proj -s python-fastapi -p /tmp/verify-proj -y
ls /tmp/verify-proj/.jvis/agents/   # Should have 8+ packs
ls /tmp/verify-proj/.claude/commands/ # Should have 8+ commands
```

## Rollback

```bash
# If something is wrong:
# 1. Yank the release on PyPI (does not delete, just hides from install)
# 2. Fix the issue
# 3. Bump to X.Y.Z+1 (PyPI doesn't allow re-uploading same version)
# 4. Re-publish
```

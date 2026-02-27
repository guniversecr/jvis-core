# PyPI Publish Guide

Step-by-step guide to publish JVIS to TestPyPI and PyPI.

## Prerequisites

- GitHub repo: `guniversecr/jvis`
- Workflow: `.github/workflows/publish-pypi.yml` (already configured)
- Local build verified: `jvis-4.0.0-py3-none-any.whl` (39 files)

## Steps

### 1. Create GitHub Environments

Go to: https://github.com/guniversecr/jvis/settings/environments

Create two environments:
- `testpypi`
- `pypi`

No special protection rules needed for testpypi. For pypi, optionally add required reviewers.

### 2. Register OIDC Trusted Publishers

#### TestPyPI

Go to: https://test.pypi.org/manage/account/publishing/

Add a new pending publisher:
- **PyPI Project Name:** `jvis`
- **Owner:** `guniversecr`
- **Repository name:** `CodeMockup`
- **Workflow name:** `publish-pypi.yml`
- **Environment name:** `testpypi`

#### PyPI

Go to: https://pypi.org/manage/account/publishing/

Add a new pending publisher:
- **PyPI Project Name:** `jvis`
- **Owner:** `guniversecr`
- **Repository name:** `CodeMockup`
- **Workflow name:** `publish-pypi.yml`
- **Environment name:** `pypi`

### 3. Publish to TestPyPI

Go to: https://github.com/guniversecr/jvis/actions/workflows/publish-pypi.yml

Click "Run workflow" -> select `testpypi` -> Run.

Wait for the workflow to complete (build -> verify -> publish).

### 4. Verify TestPyPI Install

```bash
pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ jvis
jvis --version
# Should output: JVIS Manager v4.0.0
```

Note: `--extra-index-url` is needed because TestPyPI doesn't have jvis's dependencies (click, jinja2, etc.).

### 5. Publish to PyPI

Option A: Via workflow dispatch:
- Go to Actions -> Publish to PyPI -> Run workflow -> select `pypi`

Option B: Via GitHub release (triggers automatically):
- Go to Releases -> Create new release
- Tag: `v4.0.0`
- Title: `JVIS v4.0.0 — Open Source Launch`
- Auto-generates release notes from commits

### 6. Verify PyPI Install

```bash
pip install jvis
jvis --version
# Should output: JVIS Manager v4.0.0
```

### 7. Post-Publish Checklist

- [ ] `pip install jvis` works on a clean Python 3.13 environment
- [ ] `jvis --version` returns 4.0.0
- [ ] `jvis new test-project --stack python-fastapi` creates a project
- [ ] Agents are available in `.claude/commands/` after project creation
- [ ] Update README badges if applicable

# ADR-007: Version Management — Mandatory Bumps and SSOT Map

**Status:** Approved
**Date:** 2026-02-23
**Author:** Winston - System Architect | JVIS Framework
**Triggered by:** Version bump omission in plan review — rule existed only in personal memory, not in shared project files

---

## Context

JVIS uses semantic versioning across 13+ files. The `jvis bump` command (added in v4.2.0) updates only 3 canonical files (Tier 1). The remaining 10+ files (documentation, code, tests) require manual updates.

This caused a concrete problem: a development plan proposed skipping the version bump because the rule was documented only in auto-memory (personal, not loaded by agents). Any agent without access to memory wouldn't know the rule exists.

**Why version bumping matters:**

1. **Agent identity** — Agents read version from `.jvis/version` and include it in their prompts. Stale versions cause confusion in multi-session workflows.
2. **PyPI publishing** — `pyproject.toml` version is the published artifact version. Mismatches between source and package cause installation issues.
3. **Provenance tracking** — `jvis new` and `jvis add` stamp the installed version into target projects. Incorrect stamps make debugging impossible.
4. **Test validation** — Tests assert the version string. Forgetting to update tests causes false failures.
5. **SSOT compliance** — ADR-001 mandates that every piece of data has ONE canonical source. Version data has two canonical sources (`.jvis/version` for runtime, `pyproject.toml` for packaging) with 10+ consumers that must stay synchronized.

---

## Decision

### Rule: Every Significant Commit Includes a Version Bump

**Scope:** Any commit that changes behavior, adds features, fixes bugs, or modifies principles/documentation. Excluded: typo fixes within the same session, WIP commits that will be squashed.

**Semantic versioning:**

| Level | When | Example |
|-------|------|---------|
| **PATCH** | Bug fixes, doc improvements, principle additions, config changes | 4.2.0 → 4.2.1 |
| **MINOR** | New features, new agents, new stacks, new commands | 4.2.0 → 4.3.0 |
| **MAJOR** | Breaking changes to CLI interface, agent schema, or config format | 4.2.0 → 5.0.0 |

### Three-Tier File Map (SSOT)

#### Tier 1: Canonical Sources (ALWAYS update)

These are the source of truth. Everything else references them.

| File | Location in file | Updated by `jvis bump` |
|------|-----------------|----------------------|
| `.jvis/version` | Entire file content | Yes |
| `.jvis/VERSION.yaml` | `version:` field + all `components:` entries | Yes |
| `pyproject.toml` | `version = "X.Y.Z"` under `[project]` | Yes |
| `CLAUDE.md` | Footer line: `JVIS vX.Y.Z` | No (manual) |

#### Tier 2: Documentation (ALWAYS update)

These reference the version for user-facing consistency.

| File | Location in file |
|------|-----------------|
| `CHANGELOG.md` | Add new `## [X.Y.Z]` section header |
| `docs/STATUS.md` | `**Version:**` line |
| `docs/manuals/INDEX.md` | Title line `# JVIS vX.Y.Z` |
| `docs/planning/JVIS-IDENTITY.md` | `Current State (vX.Y.Z)` — 2 occurrences + PyPI tag |

#### Tier 3: Code & Tests (ALWAYS update)

These contain version strings in source code or test assertions.

| File | Location in file | Notes |
|------|-----------------|-------|
| `tests/unit/test_cli.py` | `assert version ==` | Reads from `.jvis/version` |
| `tests/integration/test_new_project.py` | `assert version ==` | Reads from `.jvis/version` |
| `tests/unit/test_version_management.py` | `assert "X.Y.Z" in result.output` (~line 36) | Dry-run output check |

### False Positives (DO NOT update during version bumps)

These files contain version-like strings that are NOT references to the JVIS version:

| File | Lines | What it is |
|------|-------|-----------|
| `tests/unit/test_version_management.py` | ~41, 46, 51 | `_bump_semver()` input examples (e.g., `"4.1.0"`) |
| `tests/unit/test_version_management.py` | ~126-144 | `stamp_version()` test inputs |
| `src/jvis/data/stacks/*/package.json.j2` | Various | npm package versions (Svelte, Next, etc.) |
| `docs/manuals/stacks/*.md` | Various | pip package versions (pytest-cov, structlog, etc.) |

### Current Gap

`jvis bump patch|minor|major` updates **only Tier 1** files (3 of 13+). Tiers 2 and 3 require manual updates. This is a known limitation.

**Future improvement:** Extend `jvis bump` to handle all three tiers automatically. This would require:
- Regex-based find/replace for Tier 2 doc files
- AST-aware or regex replacement for Tier 3 code/test files
- A `--dry-run` flag showing all planned changes (already exists for Tier 1)

Until then, the full checklist in CLAUDE.md and this ADR serve as the manual reference.

### Commit Flow

1. Update all Tier 1, 2, and 3 files
2. `make generate` (regenerates 17 agent commands — they embed version)
3. Stage version files + generated commands
4. Commit: `chore: bump version X.Y.Z → A.B.C`
5. Push (if releasing)

---

## Consequences

### Positive
- Rule is now in CLAUDE.md (always loaded) — every agent knows it
- Complete SSOT map prevents "which files do I update?" confusion
- False positives list prevents unnecessary test fixture changes
- Future `jvis bump` improvement has a clear specification

### Negative
- Manual process for 10+ files is error-prone until `jvis bump` covers all tiers
- Adding new version-referencing files requires updating this ADR

### Risks
- **Drift:** If a new file starts referencing the version and isn't added to this ADR, it will become stale. Mitigation: QA gate should grep for the old version string after bumps.
- **Automation gap:** Until `jvis bump` handles all tiers, developers must follow the manual checklist. Mitigation: CLAUDE.md section + this ADR serve as reminders.

---

## References

- **ADR-001:** Core Principles — SSOT principle that motivates this ADR
- **Version command:** `src/jvis/commands/bump_cmd.py` — `jvis bump` implementation
- **CLAUDE.md:** Version Management section — concise checklist for daily use
- **Memory:** `MEMORY.md` — original checklist (now codified here)

---

*This document was generated using JVIS Framework*
*Agent: Winston - System Architect*
*Date: 2026-02-23*

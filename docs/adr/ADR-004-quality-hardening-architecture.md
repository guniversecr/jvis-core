# ADR-004: Quality Hardening — Technical Architecture

**Status:** Proposed
**Date:** 2026-02-15
**Author:** Winston — System Architect | JVIS Framework
**Triggered by:** Deep audit (6.2/10) → PRD `docs/product/prd-quality-hardening.md`
**Scope:** Internal refactoring. Zero public API changes. Zero new dependencies.

---

## Context

A deep audit scored JVIS 6.2/10. Five specific architectural deficiencies were identified:

1. **OCP violation in `monorepo.py`** — `_backend_dev_cmd()` has 9 hardcoded if-statements. Adding a stack means editing Python. This contradicts the project's own data-driven principle (CLAUDE.md: "Stack behavior comes from manifest.yaml, not Python code").

2. **DRY violation in `stack_selector.py`** — Four nearly identical selection loops (`_select_category`, `_select_by_language`, `_select_framework`, `_select_from_flat`) with ~20 lines of duplicated while-loop + try/except + validation logic each.

3. **Silent failures everywhere** — `registry.py:43` catches `yaml.YAMLError, KeyError, OSError` and silently continues. Only 1 of 35 modules uses `logging`. Debugging is archaeology.

4. **God-function in `primary.py`** — `new()` is 120+ lines handling both interactive and scripted flows with CC~12.

5. **Undocumented magic** — Regex constraints, heuristic thresholds, and convention choices without any "why" comments.

This ADR defines the technical approach for all 10 stories across 3 epics.

---

## Decision

### 1. Stack Manifest Schema Extension (Story 8.1)

**What changes:** Add `dev_command`, `dev_port`, and `getting_started` fields to stack manifest YAML.

**Schema addition:**

```yaml
# Added to each manifest.yaml
dev_command: "python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000"
dev_port: 8000
getting_started:
  prerequisites: "Python 3.12+"
  commands:
    - "python3.13 -m venv .venv"
    - "source .venv/bin/activate"
    - "pip install -r requirements.txt"
    - "python -m uvicorn src.main:app --port 8000"
```

**StackInfo dataclass extension:**

```python
# registry.py — add 3 fields
@dataclass
class StackInfo:
    # ... existing fields ...
    dev_command: str = ""
    dev_port: int = 8000
    getting_started: dict[str, Any] = field(default_factory=dict)
```

**Load from manifest:**

```python
# registry.py:_load_manifest() — add 3 lines
dev_command=raw.get("dev_command", ""),
dev_port=raw.get("dev_port", 8000),
getting_started=raw.get("getting_started", {}),
```

**Consumers refactored:**

| Current (hardcoded) | After (data-driven) |
|---------------------|---------------------|
| `monorepo.py:_backend_dev_cmd()` — 9 if-statements | `stack_info.dev_command` — one lookup |
| `monorepo.py:_write_docker_compose()` — hardcoded port check | `stack_info.dev_port` |
| `shared_files.py:_getting_started_section()` — 5 if-statements | `stack_info.getting_started` → Jinja2 render |
| `primary.py:_SETUP_HINTS` — 60-line dict | `stack_info.getting_started.commands` |

**Impact on `monorepo.py`:**

```python
# BEFORE (9 if-statements):
def _backend_dev_cmd(stack: str) -> str:
    if "fastapi" in stack: return "python -m uvicorn ..."
    if "django" in stack: return "python manage.py ..."
    # ... 7 more

# AFTER (1 line):
def _backend_dev_cmd(stack: StackInfo) -> str:
    return stack.dev_command or "echo 'Configure dev command in manifest.yaml'"
```

**Function signature change:** `_backend_dev_cmd(stack: str)` → `_backend_dev_cmd(stack: StackInfo)`. This requires updating `_write_docker_compose()` to receive `StackInfo` instead of `str`. The `create_monorepo_root()` signature changes accordingly.

**Impact on `shared_files.py`:**

```python
# BEFORE:
def _getting_started_section(stack_language: str) -> str:
    if stack_language == "python": return "..."
    if stack_language in ("typescript", "javascript"): return "..."

# AFTER:
def _getting_started_section(stack: StackInfo | None) -> str:
    if not stack or not stack.getting_started:
        return _GENERIC_GETTING_STARTED
    gs = stack.getting_started
    prereq = gs.get("prerequisites", "")
    commands = gs.get("commands", [])
    # Build from data
```

**Impact on `primary.py`:** `_SETUP_HINTS` dict (lines 406-464) and `_NPM_STACKS` frozenset (lines 467-479) are **deleted**. `_print_setup_hints(stack_id)` becomes `_print_setup_hints(stack: StackInfo | None)` and reads from `stack.getting_started`.

**Trade-off:** This adds 3 fields to all 17 manifest files (51 lines of YAML). The cost is low and the benefit is elimination of ~100 lines of hardcoded Python + full OCP compliance.

**Backward compatibility:** `dev_command` defaults to `""` so existing manifests without the field won't break. The code path checks `stack.dev_command or fallback`.

---

### 2. `prompt_choice()` Utility (Story 8.2)

**Location:** `src/jvis/utils/ui.py` (extend existing UI module)

**API:**

```python
from typing import Callable, TypeVar

T = TypeVar("T")

def prompt_choice(
    items: list[T],
    label: str,
    display_fn: Callable[[T], str] | None = None,
    detail_fn: Callable[[T], str] | None = None,
) -> T:
    """Display numbered menu and return the selected item.

    Args:
        items: List of items to choose from (must be non-empty).
        label: Menu prompt label (e.g. "category", "language", "framework").
        display_fn: Function to get display text for each item. Defaults to str().
        detail_fn: Optional function to get detail line below each item.

    Returns:
        The selected item from the list.
    """
```

**Implementation (core loop):**

```python
def prompt_choice(items, label, display_fn=None, detail_fn=None):
    if not items:
        raise ValueError(f"No items to select for '{label}'")
    if len(items) == 1:
        selected = items[0]
        name = display_fn(selected) if display_fn else str(selected)
        click.echo(f"  {green('✓')} {label.capitalize()}: {name}")
        return selected

    display = display_fn or str
    click.echo(f"\n  {cyan(f'Select {label}:')}\n")
    for i, item in enumerate(items, 1):
        click.echo(f"    {i}) {bold(display(item))}")
        if detail_fn:
            click.echo(f"       {detail_fn(item)}")
    click.echo("")

    while True:
        choice = click.prompt(f"  Select {label}", default="1", show_default=True)
        try:
            idx = int(choice) - 1  # 1-indexed display → 0-indexed list
            if 0 <= idx < len(items):
                selected = items[idx]
                name = display_fn(selected) if display_fn else str(selected)
                click.echo(f"  {green('✓')} {label.capitalize()}: {name}")
                return selected
        except ValueError:
            pass
        click.echo(f"  {red('Invalid')}. Enter 1-{len(items)}.")
```

**Refactored callers in `stack_selector.py`:**

```python
# _select_category → becomes:
def _select_category(categories: list[str]) -> str:
    return prompt_choice(
        categories,
        label="category",
        display_fn=lambda c: _CATEGORY_LABELS.get(c, c),
    )

# _select_by_language → becomes:
def _select_by_language(by_lang: dict[str, list[StackInfo]]) -> list[StackInfo]:
    langs = list(by_lang.keys())
    selected = prompt_choice(
        langs,
        label="language",
        display_fn=lambda l: _LANGUAGE_LABELS.get(l, l.capitalize()),
    )
    return by_lang[selected]

# _select_framework → becomes:
def _select_framework(stacks: list[StackInfo], label: str = "stack") -> StackInfo:
    return prompt_choice(
        stacks,
        label=label,
        display_fn=lambda s: s.name,
        detail_fn=lambda s: s.description,
    )

# _select_from_flat → becomes identical to _select_framework → DELETE IT
```

**Net deletion:** ~80 lines. `_select_from_flat` is eliminated entirely (it was identical to `_select_framework`).

**Why `ui.py` not a new file:** The UI module already has `cyan()`, `green()`, `red()`, `bold()` — putting `prompt_choice()` there keeps all UI primitives in one place. No new module needed.

---

### 3. Logging Architecture (Story 8.3)

**Design principle:** Minimal. Use stdlib `logging` with the standard pattern. No framework, no custom formatters, no JSON logging.

**New module: `src/jvis/log_config.py`**

```python
"""Logging configuration for JVIS CLI."""

import logging
import sys


def setup_logging(verbose: bool = False) -> None:
    """Configure logging for the JVIS CLI.

    Default: WARNING to stderr (silent for normal usage).
    Verbose: DEBUG to stderr (for debugging).
    """
    level = logging.DEBUG if verbose else logging.WARNING
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(logging.Formatter(
        "%(levelname)s [%(name)s] %(message)s"
    ))
    root = logging.getLogger("jvis")
    root.setLevel(level)
    root.addHandler(handler)
```

**Integration point — `cli.py`:**

```python
@click.group(invoke_without_command=True)
@click.option("--verbose", "-v", is_flag=True, help="Enable debug logging.")
@click.version_option(version=read_version(), prog_name="JVIS Manager")
@click.pass_context
def cli(ctx: click.Context, verbose: bool) -> None:
    """JVIS — Journey Virtual Intelligent System."""
    from jvis.log_config import setup_logging
    setup_logging(verbose=verbose)
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())
```

**Per-module pattern (applied to all 35 modules with actual logic):**

```python
import logging

logger = logging.getLogger(__name__)
```

**Skip `__init__.py` files** — They have no logic, no need for loggers. Only modules with actual code get loggers. Estimated: ~20 modules need loggers (excluding `__init__.py` and pure data files).

**Critical silent-failure fixes:**

| File | Current | After |
|------|---------|-------|
| `registry.py:43` | `except (...): continue` | `logger.warning("Skipping invalid manifest: %s (%s)", manifest_path, e)` |
| `framework.py` | `except (...): continue` | `logger.warning("Failed to load stack %s: %s", path.name, e)` |
| `detection/project_state.py` | `except (PermissionError, OSError): continue` | `logger.debug("Cannot read %s: %s", path, e)` |
| `detection/tech_stack.py` | silent file reads | `logger.debug("Detected: %s", ...)` |

**Rule:** `logger.warning()` for skipped items that the user might care about. `logger.debug()` for expected conditions (file not found during detection is normal). Never `logger.error()` for recoverable situations.

**Distinction from `click.echo()`:** `click.echo()` is for **intended user output** (progress messages, results, prompts). `logger` is for **diagnostic information** (what was skipped, why, what failed). They serve different audiences and must not be mixed.

---

### 4. `primary.py` Refactoring Strategy (Story 8.4)

**Current state:** 509 lines, `new()` is 120+ lines with CC~12. Two logically separate flows (interactive vs scripted) are interleaved in one function.

**Target architecture:**

```
new()                          # Click decorator, dispatch
├── _create_project_scripted() # Non-interactive: validate flags, build config
├── _create_project_interactive() # Interactive: prompts, selection
└── _scaffold_project()        # Shared: file creation, git, docs, hints
```

**Specific extraction:**

```python
@click.command()
@click.option(...)
def new(name, stack, dest_path, db, yes):
    """Create a new JVIS project."""
    click.echo(ui.header("JVIS Project Initializer"))

    if name and stack and dest_path:
        config = _create_project_scripted(name, stack, dest_path, db)
    else:
        config = _create_project_interactive()

    if not yes and not show_summary_and_confirm(**config):
        click.echo(f"\n  {ui.yellow('Cancelled.')}")
        raise SystemExit(0)

    _scaffold_project(**config)
```

**`ProjectConfig` dataclass** (replaces the loose variables):

```python
@dataclass
class ProjectConfig:
    project_name: str
    project_description: str
    project_dir: Path
    project_type: str
    stacks: dict[str, StackInfo | None]
    database: str
```

**Why a dataclass, not a dict:** Type safety. The current code passes `stacks: dict[str, StackInfo | None]` which has no contract. A dataclass makes the shape explicit and MyPy-checkable.

**Line count target:** `new()` → 15 lines. `_create_project_scripted()` → 30 lines. `_create_project_interactive()` → 20 lines. `_scaffold_project()` → 60 lines. `_print_post_install()` → 20 lines. Total primary.py: ~380 lines (down from 509). `add()` stays as-is (it's already reasonable at ~80 lines).

**No behavior changes.** This is pure extraction refactoring. Every test must pass unchanged.

---

### 5. Agent Consolidation Approach (Story 10.2)

**Principle:** Consolidate by **domain**, not by deleting. Merged agents inherit all unique commands from their sources.

**Payment agents:**

```
BEFORE: /stripe (24 commands) + /paypal (24 commands) + /square (24 commands)
AFTER:  /payments (30 commands, provider parameter)
```

**Implementation in YAML:**

```yaml
# .jvis/agents/integrations/payments.yaml
agent:
  id: payments
  name: "Payments Integration Architect"
  customization: |
    This agent handles Stripe, PayPal, and Square integrations.
    Ask user which payment provider they're using before executing commands.
    Provider-specific commands are prefixed with the provider name.
commands:
  # Shared (applies to all providers)
  - setup-payments: "Configure payment processing for selected provider"
  - webhook-config: "Set up payment webhooks"
  - test-payments: "Run payment integration tests"
  # Provider-specific (inherited from originals, deduplicated)
  - stripe-setup: "Initialize Stripe SDK and keys"
  - paypal-setup: "Initialize PayPal SDK and credentials"
  - square-setup: "Initialize Square SDK and credentials"
  # ... remaining unique commands
```

**Marketing agents consolidation:**

| Before (13 agents) | After (6 agents) | Merge rationale |
|---------------------|-------------------|-----------------|
| `/brand` + `/creative-director` | `/brand` | 80% overlap, both do brand strategy |
| `/copywriter` + `/content-writer` | `/content` | Both produce written content |
| `/social-media` + `/community` | `/social` | Both manage social presence |
| `/seo` + `/analytics` | `/seo-analytics` | Both deal with search + data |
| `/comms` + `/pr` | `/comms` | Both handle external communications |
| `/influencer` | `/influencer` | Unique enough to keep |

**Process:**
1. For each merge: union of all commands, deduplicate
2. Write new consolidated YAML
3. Delete old YAML files
4. Run `make generate` to regenerate slash commands
5. Update `.claude/commands/` (generated output, not manual)

**SSOT preserved:** Agent YAML configs are the source. Generated commands are outputs.

---

### 6. Error Recovery Architecture (Story 9.2)

**Principle:** Every `except` block must either (a) log and continue, or (b) raise a clear error. No silent swallowing.

**New error behaviors (enabled by Story 8.3 logging):**

| Scenario | Current behavior | New behavior |
|----------|-----------------|--------------|
| Broken Jinja2 template | `SandboxedEnvironment` raises, caller may catch | Let exception propagate with template path in message |
| Missing template file | `logger.warning()` + skip (already exists) | Keep as-is (correct behavior) |
| Permission denied on output | `OSError` propagates unhandled | Catch at `_scaffold_project()` level, clean error message |
| Malformed YAML manifest | `except (yaml.YAMLError, ...): continue` | `logger.warning()` with file path + YAML error details |
| Empty `dev_command` | N/A (new field) | Default to empty string, code uses `or` fallback |
| Jinja2 injection in project name | Rendered literally into templates | Already mitigated: `validate_project_name()` rejects `{{`, `{%` via regex `^[a-z][a-z0-9_-]{1,63}$` |

**Test structure for error recovery:**

```python
# tests/unit/test_error_recovery.py
class TestBrokenTemplates:
    def test_invalid_jinja2_syntax_raises_clear_error(self, tmp_path): ...
    def test_missing_template_file_logs_warning(self, tmp_path, caplog): ...
    def test_malformed_yaml_manifest_logs_warning(self, tmp_path, caplog): ...

class TestPermissionErrors:
    def test_readonly_output_dir_raises_clear_error(self, tmp_path): ...
    def test_no_partial_files_on_permission_error(self, tmp_path): ...

class TestInputValidation:
    def test_project_name_with_jinja2_syntax_rejected(self): ...
    def test_empty_dev_command_uses_fallback(self, tmp_path): ...
    def test_missing_getting_started_uses_generic(self, tmp_path): ...
```

---

### 7. Story Sequencing — Dependency Graph

```
Story 8.3 (logging)     ← FIRST: All subsequent stories benefit from logging
  ↓
Story 8.1 (manifests)   ← Changes StackInfo dataclass, touches monorepo + shared_files
  ↓
Story 8.2 (prompt_choice) ← Independent, but uses logging
  ↓
Story 8.4 (primary.py)  ← Depends on 8.1 (manifest changes propagate to primary.py)
  ↓
Story 8.5 (comments)    ← Last in Epic 8: document what was built
  ↓
Story 9.1 (vanity tests) ← Clean up tests that may break from refactoring
  ↓
Story 9.2 (error tests)  ← New tests validate logging + error behavior
  ↓
Story 10.1 (agent counts) ← Update docs with honest numbers
  ↓
Story 10.2 (consolidate)  ← Merge agents, regenerate
  ↓
Story 10.3 (README)       ← LAST: Reflects final state of everything above
```

**Rationale for reordering from PRD:**
- PRD had 8.1 first, but logging (8.3) should be first so that 8.1's manifest changes get proper `logger.warning()` from day one
- 8.4 depends on 8.1 because `primary.py:_SETUP_HINTS` is deleted when manifests take over
- 8.5 is last in Epic 8 because you document what exists, not what you plan to build

---

## Consequences

### Positive
- OCP restored: Adding a stack = one YAML file, zero Python edits
- DRY restored: One `prompt_choice()` instead of 4 duplicate loops
- Observable: Every silent failure now logged with context
- Testable: `_scaffold_project()` is independently testable
- Honest: Agent counts reflect reality

### Negative
- 17 manifest files need 3 new fields each (~51 lines of YAML to write)
- `create_monorepo_root()` signature changes — callers must update
- Test count may decrease (vanity removal) — team must accept this

### Risks
- `prompt_choice()` TypeVar generic may need `# type: ignore` in edge cases with MyPy strict
- Agent consolidation may break user workflows if they reference `/stripe` by name in their own scripts

### Mitigations
- TypeVar: Test with MyPy before committing. If issues, use `Any` return and cast at call site
- Agent refs: Add deprecation aliases (symlinks from old command names to new) for one release cycle

---

## Files Modified (Complete List)

### Epic 8 — Code Quality
| Story | Files Modified | Files Created |
|-------|---------------|---------------|
| 8.3 | `cli.py`, + 20 modules (add `logger`) | `src/jvis/log_config.py` |
| 8.1 | `registry.py`, `monorepo.py`, `shared_files.py`, `primary.py`, 17× `manifest.yaml` | — |
| 8.2 | `utils/ui.py`, `core/stack_selector.py` | — |
| 8.4 | `commands/primary.py` | — |
| 8.5 | `validation.py`, `project_state.py`, `shared_files.py`, `stack_selector.py`, + ~10 others | — |

### Epic 9 — Tests
| Story | Files Modified | Files Created |
|-------|---------------|---------------|
| 9.1 | `test_cli.py`, `test_mcp_servers.py`, `test_new_project.py`, + others | — |
| 9.2 | — | `tests/unit/test_error_recovery.py` |

### Epic 10 — Documentation
| Story | Files Modified | Files Created |
|-------|---------------|---------------|
| 10.1 | `README.md`, `CLAUDE.md`, `docs/STATUS.md` | — |
| 10.2 | Agent YAML files, `.claude/commands/` (regenerated) | Consolidated YAML files |
| 10.3 | `README.md` | — |

---

*Generated by Winston — System Architect | JVIS Framework*
*Date: 2026-02-15*

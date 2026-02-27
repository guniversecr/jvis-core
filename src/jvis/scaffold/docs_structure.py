"""Create the standard JVIS docs/ directory structure."""

from __future__ import annotations

import logging
import subprocess
from datetime import date
from pathlib import Path

from jvis.utils.fs import mkdir_p, write_file

logger = logging.getLogger(__name__)

# Agent names for inter-agent note files
_AGENTS = [
    ("analyst", "Analyst (Mary)"),
    ("pm", "PM (John)"),
    ("architect", "Architect (Winston)"),
    ("sm", "SM (Bob)"),
    ("dev", "Dev (James)"),
    ("qa", "QA (Quinn)"),
    ("devsecops", "DevSecOps (SecOps)"),
]


def create_docs_structure(project_dir: Path) -> None:
    """Create docs/, docs/notes/, docs/security/, docs/qa/, etc."""
    _create_notes(project_dir)
    _create_security_docs(project_dir)
    _create_other_dirs(project_dir)


def _create_notes(project_dir: Path) -> None:
    notes = project_dir / "docs" / "notes"
    mkdir_p(notes)

    today = date.today().isoformat()

    write_file(
        notes / "project-log.md",
        f"""\
# Project Log

Central log for project activities. Entries older than 7 days should be cleaned.

---

## [{today}] - Project Initialized

**Agent:** System
**Action:** Project created with JVIS framework

---
""",
    )

    write_file(
        notes / "lessons-learned.md",
        """\
# Lessons Learned

Permanent knowledge repository. These lessons should NEVER be deleted.

---
""",
    )

    write_file(
        notes / "next-action.md",
        """\
# Next Actions

Pending actions for agents.

## Pending Actions

### For PM:
- [ ] Create PRD

### For Architect:
- [ ] Define architecture

### For Dev:
- [ ] Implement first story
""",
    )

    # Per-agent note files
    for agent_id, agent_name in _AGENTS:
        write_file(
            notes / f"from-{agent_id}.md",
            f"""\
# Notes from {agent_name}

Communication from the {agent_name} agent to other agents.
Entries older than 14 days should be cleaned.

---
""",
        )


def _create_security_docs(project_dir: Path) -> None:
    sec = project_dir / "docs" / "security"
    for sub in ("plans", "audits", "threat-models", "vulnerabilities", "compliance", "incidents"):
        mkdir_p(sec / sub)

    write_file(
        sec / "README.md",
        """\
# Security Documentation

## Structure

- **plans/** — Security implementation plans
- **audits/** — Security audit reports
- **threat-models/** — STRIDE threat models
- **vulnerabilities/** — Vulnerability reports
- **compliance/** — Compliance documentation (OWASP, etc.)
- **incidents/** — Security incident reports
""",
    )


def _create_other_dirs(project_dir: Path) -> None:
    mkdir_p(project_dir / "docs" / "stories")
    mkdir_p(project_dir / "docs" / "qa" / "gates")
    mkdir_p(project_dir / "docs" / "qa" / "assessments")
    mkdir_p(project_dir / "docs" / "architecture")


# ---------------------------------------------------------------------------
# Context Map generation
# ---------------------------------------------------------------------------


def create_context_map(
    project_path: Path,
    stack: str,
    database: str,
    language: str,
) -> None:
    """Generate ``docs/notes/context-map.md`` with YAML front-matter."""
    main_branch = _detect_git_branch(project_path)
    remote = _detect_git_remote(project_path)
    directories = _detect_directories(project_path)
    today = date.today().isoformat()

    content = _render_context_map(
        project_root=str(project_path),
        main_branch=main_branch,
        remote=remote,
        primary_language=language,
        stack=stack,
        database=database,
        last_updated=today,
        directories=directories,
    )

    dest = project_path / "docs" / "notes" / "context-map.md"
    mkdir_p(dest.parent)
    write_file(dest, content)


def _detect_git_branch(project_path: Path) -> str:
    """Return the current default branch name, or ``'main'`` as fallback."""
    try:
        result = subprocess.run(
            ["git", "symbolic-ref", "--short", "HEAD"],
            cwd=project_path,
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError) as exc:
        logger.debug("Cannot detect git branch in %s: %s", project_path, exc)
    return "main"


def _detect_git_remote(project_path: Path) -> str:
    """Return the origin remote URL, or ``'not configured'`` as fallback."""
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            cwd=project_path,
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError) as exc:
        logger.debug("Cannot detect git remote in %s: %s", project_path, exc)
    return "not configured"


def _detect_directories(project_path: Path) -> list[str]:
    """Return a sorted list of top-level directories (excluding hidden ones)."""
    dirs: list[str] = []
    try:
        for entry in sorted(project_path.iterdir()):
            if entry.is_dir() and not entry.name.startswith("."):
                dirs.append(entry.name + "/")
    except OSError as exc:
        logger.debug("Cannot list directories in %s: %s", project_path, exc)
    return dirs


def _render_context_map(
    *,
    project_root: str,
    main_branch: str,
    remote: str,
    primary_language: str,
    stack: str,
    database: str,
    last_updated: str,
    directories: list[str],
) -> str:
    """Render YAML-front-matter + Markdown body for the context map."""
    lines: list[str] = [
        "---",
        f'project_root: "{project_root}"',
        f'main_branch: "{main_branch}"',
        f'remote: "{remote}"',
        f'primary_language: "{primary_language}"',
        f'stack: "{stack}"',
        f'database: "{database}"',
        f'last_updated: "{last_updated}"',
        "---",
        "",
        "# Project Context Map",
        "",
        "Structured reference for agent context loading.",
        "This file is auto-generated by JVIS and updated by `*save-context`.",
        "",
        "## Directory Structure",
        "",
    ]

    if directories:
        lines.append("```")
        for d in directories:
            lines.append(d)
        lines.append("```")
    else:
        lines.append("_No directories detected yet._")

    lines.append("")
    return "\n".join(lines)

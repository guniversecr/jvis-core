"""Copy the JVIS framework files (.jvis/, .claude/, CLAUDE.md) into a project."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import TypedDict

from jvis.utils.fs import copy_file, copy_tree, mkdir_p, write_file
from jvis.utils.paths import get_data_dir, get_jvis_home, get_repo_root

logger = logging.getLogger(__name__)

# Essential subdirectories inside .jvis/ to copy
_JVIS_DIRS = (
    "agents",
    "templates",
    "workflows",
    "utils",
    "journey",
    "agent-engine",
)

# Essential files inside .jvis/ to copy
_JVIS_FILES = (
    "core-config.yaml",
    "version",
    "VERSION.yaml",
    "user-guide.md",
    "install-manifest.yaml",
)


# Platform-specific output directories.
# Each AI coding assistant uses a different convention for custom commands/rules:
# - Claude Code: .claude/commands/*.md  (slash commands)
# - Cursor:      .cursor/rules/*.mdc    (rule files, .mdc = markdown-cursor)
# - Kiro:        .kiro/steering/*.md     (steering docs)
class _PlatformConfig(TypedDict):
    commands_dir: str
    config_file: str | None


_PLATFORM_DIRS: dict[str, _PlatformConfig] = {
    "claude": {
        "commands_dir": ".claude/commands",
        "config_file": "CLAUDE.md",
    },
    "cursor": {
        "commands_dir": ".cursor/rules",
        "config_file": None,
    },
    "kiro": {
        "commands_dir": ".kiro/steering",
        "config_file": "AGENTS.md",
    },
}

# Maps platform name to the repo-root-relative directory containing generated commands
_PLATFORM_REPO_DIRS = {
    "claude": ".claude/commands",
    "cursor": ".cursor/rules",
    "kiro": ".kiro/steering",
}

# Subdirectories inside .claude/ to copy (beyond commands/)
# Bug #3 and #4: skills/ and hooks/ were never copied to target projects
_CLAUDE_EXTRA_DIRS = ("skills", "hooks")


def install_framework(project_dir: Path) -> None:
    """Copy JVIS framework files from package data into *project_dir*.

    Raises ``RuntimeError`` when the critical ``.jvis/`` source directory
    cannot be found (callers in the CLI layer will surface this to the user).
    """
    data = get_data_dir()
    if not _copy_jvis_dir(data, project_dir):
        msg = (
            "JVIS framework source (.jvis/) not found. "
            "The package may be incomplete. Reinstall with: pip install --force-reinstall jvis"
        )
        raise RuntimeError(msg)
    _copy_platform_files(data, project_dir)
    _copy_claude_extras(data, project_dir)
    _copy_claude_md(data, project_dir)


def _resolve_jvis_source(data: Path) -> Path | None:
    """Find the .jvis/ source directory across all possible locations.

    Search order:
    1. Package data (installed wheel via force-include)
    2. Repository root (editable install / dev mode)
    3. JVIS_HOME environment variable
    """
    # 1. Installed mode: data/.jvis/ (Hatchling force-include puts it here)
    candidate = data / ".jvis"
    if candidate.is_dir():
        return candidate

    # 2. Dev mode: repo root has .jvis/
    candidate = get_repo_root() / ".jvis"
    if candidate.is_dir():
        return candidate

    # 3. JVIS_HOME fallback
    candidate = get_jvis_home() / ".jvis"
    if candidate.is_dir():
        return candidate

    return None


def _copy_jvis_dir(data: Path, project_dir: Path) -> bool:
    """Copy .jvis/ essential dirs and files.

    Returns ``True`` on success, ``False`` when the source cannot be found.
    """
    src_jvis = _resolve_jvis_source(data)

    if src_jvis is None:
        logger.error(
            "Cannot find JVIS framework source (.jvis/ directory). Checked: %s/.jvis, %s/.jvis, %s/.jvis.",
            data,
            get_repo_root(),
            get_jvis_home(),
        )
        return False

    logger.info("Copying .jvis/ from %s to %s", src_jvis, project_dir)

    dst_jvis = project_dir / ".jvis"
    mkdir_p(dst_jvis)

    copied = 0
    for dirname in _JVIS_DIRS:
        src = src_jvis / dirname
        if src.is_dir():
            copy_tree(src, dst_jvis / dirname)
            copied += 1
            logger.debug("Copied .jvis/%s/", dirname)
        else:
            logger.debug("Skipping .jvis/%s/ (not found in source)", dirname)

    for filename in _JVIS_FILES:
        src = src_jvis / filename
        if src.is_file():
            copy_file(src, dst_jvis / filename)
            copied += 1
            logger.debug("Copied .jvis/%s", filename)

    logger.info("Copied %d items from .jvis/ to %s", copied, project_dir)
    return True


def _resolve_platform_source(data: Path, platform: str) -> Path | None:
    """Find the platform commands source directory."""
    # Installed mode: data/commands/ (force-include puts platform files here)
    candidate = data / "commands"
    if candidate.is_dir():
        return candidate

    # Dev mode: commands live at repo root under platform-specific dir
    repo_dir = _PLATFORM_REPO_DIRS.get(platform)
    if repo_dir:
        candidate = get_repo_root() / repo_dir
        if candidate.is_dir():
            return candidate

    return None


def _copy_platform_files(data: Path, project_dir: Path) -> None:
    """Copy platform-specific command/rule/steering files for all available platforms."""
    for platform, cfg in _PLATFORM_DIRS.items():
        _copy_platform_commands(data, project_dir, platform, cfg["commands_dir"])


def _copy_platform_commands(
    data: Path,
    project_dir: Path,
    platform: str,
    commands_rel: str,
) -> None:
    """Copy command files for a single platform if they exist."""
    commands_src = _resolve_platform_source(data, platform)
    if commands_src is None:
        logger.debug("No commands found for platform '%s'", platform)
        return

    dst = project_dir / commands_rel
    mkdir_p(dst)

    # Copy command files (*.md or *.mdc depending on platform)
    for pattern in ("*.md", "*.mdc"):
        for src_file in sorted(commands_src.glob(pattern)):
            copy_file(src_file, dst / src_file.name)

    # Bug #5 fix: copy ALL subdirectories (workflows/, journey/, etc.)
    # Previously only workflows/ was copied, missing journey/
    for subdir in sorted(commands_src.iterdir()):
        if subdir.is_dir():
            copy_tree(subdir, dst / subdir.name)
            logger.debug("Copied %s/%s/", commands_rel, subdir.name)


def _copy_claude_extras(data: Path, project_dir: Path) -> None:
    """Copy .claude/skills/ and .claude/hooks/ to project.

    Bug #3 and #4 fix: these directories were never copied to target projects.
    """
    repo = get_repo_root()

    for dirname in _CLAUDE_EXTRA_DIRS:
        # Try installed mode first (data/<dirname>/)
        src = data / dirname
        if not src.is_dir():
            # Dev mode: repo root .claude/<dirname>/
            src = repo / ".claude" / dirname
        if not src.is_dir():
            logger.debug(".claude/%s/ not found, skipping", dirname)
            continue

        dst = project_dir / ".claude" / dirname
        copy_tree(src, dst)
        logger.debug("Copied .claude/%s/", dirname)


def _copy_claude_md(data: Path, project_dir: Path) -> None:
    """Copy or generate CLAUDE.md for the project."""
    dst = project_dir / "CLAUDE.md"
    if dst.exists():
        return  # Don't overwrite existing

    # Try bundled template first
    template = data / "templates" / "CLAUDE.md.j2"
    if template.is_file():
        _render_claude_md(template, dst, project_dir.name)
        return

    # Try copying from repo root (dev mode)
    repo_claude = get_repo_root() / "CLAUDE.md"
    if repo_claude.is_file():
        copy_file(repo_claude, dst)
        return

    # Fallback: generate minimal CLAUDE.md
    write_file(dst, _MINIMAL_CLAUDE_MD)

    # Also generate AGENTS.md for Kiro compatibility
    _generate_agents_md(data, project_dir)


def _render_claude_md(template_path: Path, dst: Path, project_name: str) -> None:
    from jinja2.sandbox import SandboxedEnvironment

    env = SandboxedEnvironment()
    tmpl = env.from_string(template_path.read_text())
    content = tmpl.render(project_name=project_name)
    write_file(dst, content)


def _generate_agents_md(data: Path, project_dir: Path) -> None:
    """Generate AGENTS.md for Kiro compatibility if template exists."""
    agents_md_dst = project_dir / "AGENTS.md"
    if agents_md_dst.exists():
        return

    template = data / "templates" / "AGENTS.md.j2"
    if template.is_file():
        from jinja2.sandbox import SandboxedEnvironment

        env = SandboxedEnvironment()
        tmpl = env.from_string(template.read_text())
        content = tmpl.render(project_name=project_dir.name)
        write_file(agents_md_dst, content)


_MINIMAL_CLAUDE_MD = """\
# CLAUDE.md

## Project Overview

This project uses JVIS for AI-assisted development.

## Development Workflow

1. `/pm` — Create PRD
2. `/architect` — Design architecture
3. `/sm` — Create stories
4. `/dev` — Implement
5. `/qa` — Review & quality gates

## Agent Commands

All agents support:
- `*help` — Show available commands
- `*load-context` — Load project context
- `*save-context` — Save session
- `*exit` — Leave agent mode

## References

- Agent configs: `.jvis/agents/`
- Inter-agent docs: `docs/notes/`
- Security docs: `docs/security/`
"""

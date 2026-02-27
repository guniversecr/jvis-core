"""Detect the current state of a project directory.

States (most specific wins):
  - ``has_context`` — JVIS installed with active work (project-log, agent notes)
  - ``has_aicore``  — JVIS installed but no significant context
  - ``has_code``    — Source code present, no JVIS
  - ``has_ideation``— Research/ideation docs but no code
  - ``empty``       — Nothing meaningful
"""

from __future__ import annotations

import logging
from pathlib import Path

logger = logging.getLogger(__name__)

# Source-code indicators: file extensions for mainstream programming languages.
# Used for a quick "does this directory have code?" check. Not exhaustive —
# covers the languages JVIS generates stacks for plus common adjacent languages.
_CODE_MARKERS = (
    "*.py",
    "*.js",
    "*.ts",
    "*.rs",
    "*.go",
    "*.java",
    "*.kt",
    "*.swift",
    "*.rb",
    "*.php",
    "*.cs",
    "*.cpp",
    "*.c",
    "*.h",
)

_CODE_CONFIG_FILES = (
    "pyproject.toml",
    "package.json",
    "Cargo.toml",
    "go.mod",
    "pom.xml",
    "build.gradle",
    "Gemfile",
    "composer.json",
    "Makefile",
    "CMakeLists.txt",
)

# Ideation/research markers
_IDEATION_FILES = (
    "market-research.md",
    "market-scan.md",
    "competitor-analysis.md",
    "winning-product-score.md",
    "idea-score.md",
    "pmf-scorecard.md",
    "business-model-canvas.md",
    "lean-canvas.md",
)

_IDEATION_DIRS = (
    "proposals",
    "workshops",
    "discovery",
    "research",
    "solution-design",
    "ideation",
)


def detect_project_state(target: Path) -> str:
    """Return the state of the directory: empty/has_ideation/has_code/has_aicore/has_context."""
    if not target.is_dir():
        return "empty"

    # Check for JVIS with context
    if _has_context(target):
        return "has_context"

    # Check for JVIS installed
    if (target / ".jvis").is_dir():
        return "has_aicore"

    # Check for source code
    if _has_source_code(target):
        return "has_code"

    # Check for ideation docs
    if _has_ideation(target):
        return "has_ideation"

    return "empty"


def get_jvis_version(target: Path) -> str:
    """Read the JVIS version from a project directory."""
    version_file = target / ".jvis" / "version"
    try:
        return version_file.read_text().strip()
    except (FileNotFoundError, PermissionError) as exc:
        logger.debug("Cannot read JVIS version from %s: %s", version_file, exc)
        return "unknown"


def _has_context(target: Path) -> bool:
    """Return True if the project has JVIS with active context."""
    jvis_dir = target / ".jvis"
    if not jvis_dir.is_dir():
        return False

    notes_dir = target / "docs" / "notes"
    if not notes_dir.is_dir():
        return False

    # Check for project-log with actual entries (not just the empty template).
    # Template has exactly 2 "---" markers (YAML frontmatter delimiters).
    # More than 2 means an agent has written session entries (each separated by "---").
    project_log = notes_dir / "project-log.md"
    if project_log.is_file():
        try:
            content = project_log.read_text()
            if content.count("---") > 2:
                return True
        except (PermissionError, OSError) as exc:
            logger.debug("Cannot read project log %s: %s", project_log, exc)

    # Check for agent notes with content.
    # Agent note files (from-dev.md, from-qa.md, etc.) have 1 "---" from
    # their template header. More than 1 means an agent wrote a handoff note.
    for f in notes_dir.iterdir():
        if f.name.startswith("from-") and f.is_file():
            try:
                content = f.read_text()
                if content.count("---") > 1:
                    return True
            except (PermissionError, OSError) as exc:
                logger.debug("Cannot read agent note %s: %s", f, exc)
                continue

    return False


def _has_source_code(target: Path) -> bool:
    """Return True if the directory contains source code."""
    # Check config files first (fast)
    for name in _CODE_CONFIG_FILES:
        if (target / name).is_file():
            return True

    # Check common source directories — these are the conventional top-level dirs
    # across Python (src/), Ruby/Node (lib/), Rails/Laravel (app/), and JVIS monorepos (server/, client/).
    for src_dir_name in ("src", "lib", "app", "server", "client"):
        src_dir = target / src_dir_name
        if src_dir.is_dir():
            for pattern in _CODE_MARKERS:
                if any(src_dir.rglob(pattern)):
                    return True

    # Check top-level source files (limit depth)
    return any(any(target.glob(pattern)) for pattern in _CODE_MARKERS)


def _has_ideation(target: Path) -> bool:
    """Return True if the directory has ideation/research documents."""
    search_roots = [target, target / "docs"]
    for root in search_roots:
        if not root.is_dir():
            continue
        for name in _IDEATION_FILES:
            if (root / name).is_file():
                return True
        for name in _IDEATION_DIRS:
            d = root / name
            if d.is_dir() and any(d.iterdir()):
                return True
    return False

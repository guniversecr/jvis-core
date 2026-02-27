"""Git helpers — init, detection, .gitignore management."""

from __future__ import annotations

import logging
import subprocess
from pathlib import Path

from jvis.utils.fs import mkdir_p, write_file

logger = logging.getLogger(__name__)


def is_git_repo(path: Path) -> bool:
    """Return True if *path* is inside a git repository."""
    try:
        result = subprocess.run(
            ["git", "-C", str(path), "rev-parse", "--is-inside-work-tree"],
            capture_output=True,
            text=True,
        )
        return result.returncode == 0
    except FileNotFoundError:
        return False


def git_init(path: Path) -> bool:
    """Initialize a git repository at *path*. Returns True on success."""
    mkdir_p(path)
    try:
        result = subprocess.run(
            ["git", "init", str(path)],
            capture_output=True,
            text=True,
        )
        return result.returncode == 0
    except FileNotFoundError:
        return False


# Standard .gitignore content for JVIS projects
_GITIGNORE_SECTIONS: dict[str, str] = {
    "general": """\
# OS
.DS_Store
Thumbs.db

# IDE
.idea/
.vscode/
*.swp
*.swo
*~

# Environment
.env
.env.local
.env.*.local
""",
    "jvis": """\
# JVIS internal (optional — track if you want version-controlled agent config)
# docs/notes/
""",
    "python": """\
# Python
__pycache__/
*.py[cod]
*.egg-info/
dist/
build/
.venv/
venv/
.mypy_cache/
.ruff_cache/
.pytest_cache/
""",
    "node": """\
# Node.js
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.next/
""",
    "rust": """\
# Rust
target/
Cargo.lock
""",
}


def write_gitignore(path: Path, sections: list[str] | None = None) -> None:
    """Write a .gitignore file with the requested sections.

    If *sections* is None, writes only the ``general`` section.
    """
    if sections is None:
        sections = ["general"]

    parts = []
    for name in sections:
        block = _GITIGNORE_SECTIONS.get(name)
        if block:
            parts.append(block)

    content = "\n".join(parts) + "\n"
    write_file(path / ".gitignore", content)


def setup_git(project_dir: Path, stack_id: str = "") -> None:
    """Initialize git and write a sensible .gitignore for the stack."""
    if not is_git_repo(project_dir):
        git_init(project_dir)

    sections = ["general", "jvis"]

    # Match stack IDs to .gitignore sections using substring checks on the stack ID.
    # Stack IDs like "python-fastapi", "nodejs-express", "rust-axum" contain the language
    # or framework name, so simple substring matching covers all current stacks.
    stack_lower = stack_id.lower()
    if "python" in stack_lower or "flask" in stack_lower or "fastapi" in stack_lower:
        sections.append("python")
    if "node" in stack_lower or "express" in stack_lower or "react" in stack_lower:
        sections.append("node")
    if "rust" in stack_lower or "axum" in stack_lower:
        sections.append("rust")

    write_gitignore(project_dir, sections)

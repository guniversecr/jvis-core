"""Post-processing entity rename — replace hardcoded 'item' with a custom entity name."""

from __future__ import annotations

import logging
from pathlib import Path

from jvis.utils.naming import entity_replacements

logger = logging.getLogger(__name__)

SKIP_EXTENSIONS = frozenset({".pyc", ".pyo", ".whl", ".egg", ".so", ".dll", ".dylib"})
SKIP_DIRS = frozenset({".git", ".venv", "node_modules", "__pycache__", ".mypy_cache"})


def apply_entity_name(target_dir: Path, entity_name: str) -> None:
    """Replace hardcoded 'item' entity with *entity_name* in all generated files.

    Three passes (bottom-up to avoid path invalidation):
      1. Replace file content
      2. Rename files with 'item' in their name
      3. Rename directories with 'item' in their name (deepest first)
    """
    if entity_name == "item":
        return

    replacements = entity_replacements("item", entity_name)
    if not replacements:
        return

    all_files = sorted(target_dir.rglob("*"), reverse=True)

    # Pass 1: replace file content
    for path in all_files:
        if not path.is_file():
            continue
        if _should_skip(path, target_dir):
            continue
        _replace_content(path, replacements)

    # Pass 2: rename files
    for path in sorted(target_dir.rglob("*"), reverse=True):
        if not path.is_file():
            continue
        if _should_skip(path, target_dir):
            continue
        _rename_path(path, replacements)

    # Pass 3: rename directories (deepest first — already reverse-sorted)
    for path in sorted(target_dir.rglob("*"), reverse=True):
        if not path.is_dir():
            continue
        if _should_skip(path, target_dir):
            continue
        _rename_path(path, replacements)


def _should_skip(path: Path, root: Path) -> bool:
    """Return True if path is inside a skip directory or has a skip extension."""
    rel_parts = path.relative_to(root).parts
    if any(part in SKIP_DIRS for part in rel_parts):
        return True
    return path.is_file() and path.suffix in SKIP_EXTENSIONS


def _replace_content(path: Path, replacements: list[tuple[str, str]]) -> None:
    """Replace entity name variants in file content."""
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, PermissionError):
        return

    new_text = text
    for old, new in replacements:
        new_text = new_text.replace(old, new)

    if new_text != text:
        path.write_text(new_text, encoding="utf-8")


def _rename_path(path: Path, replacements: list[tuple[str, str]]) -> None:
    """Rename a file or directory if its name contains an entity variant."""
    name = path.name
    new_name = name
    for old, new in replacements:
        new_name = new_name.replace(old, new)

    if new_name != name:
        new_path = path.parent / new_name
        path.rename(new_path)

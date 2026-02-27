"""Filesystem helpers — safe directory/file creation and copying."""

from __future__ import annotations

import logging
import os
import shutil
from pathlib import Path

logger = logging.getLogger(__name__)


def mkdir_p(path: Path) -> None:
    """Create directory and parents (like ``mkdir -p``)."""
    path.mkdir(parents=True, exist_ok=True)


def write_file(path: Path, content: str) -> None:
    """Write *content* to *path*, creating parent directories as needed."""
    mkdir_p(path.parent)
    path.write_text(content, encoding="utf-8")


def copy_tree(src: Path, dst: Path) -> None:
    """Recursively copy *src* directory to *dst*, merging into existing."""
    if not src.is_dir():
        return
    shutil.copytree(src, dst, dirs_exist_ok=True)


def copy_file(src: Path, dst: Path) -> None:
    """Copy a single file, creating destination directory if needed."""
    mkdir_p(dst.parent)
    shutil.copy2(src, dst)


def is_empty_dir(path: Path) -> bool:
    """Return True if *path* is an existing directory with no entries."""
    if not path.is_dir():
        return False
    try:
        return not any(path.iterdir())
    except PermissionError:
        return False


def is_writable(path: Path) -> bool:
    """Return True if *path* (file or directory) is writable."""
    return os.access(path, os.W_OK)

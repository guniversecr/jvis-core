"""JVIS path resolution — locates JVIS_HOME and data directories."""

from __future__ import annotations

import logging
import os
from functools import lru_cache
from pathlib import Path

logger = logging.getLogger(__name__)

# Package root: src/jvis/ (parent of utils/)
_PKG_ROOT = Path(__file__).resolve().parent.parent


@lru_cache(maxsize=1)
def get_repo_root() -> Path:
    """Return the repository root directory (dev mode).

    In development layout: src/jvis/utils/paths.py is 3 levels below repo root
    (src/jvis/utils/ → src/jvis/ → src/ → repo root).
    """
    return _PKG_ROOT.parent.parent


def get_jvis_home() -> Path:
    """Locate the JVIS root directory.

    Search order:
    1. JVIS_HOME environment variable
    2. Repository root (development / editable install)
    3. Package data bundled via hatch build
    """
    env_home = os.environ.get("JVIS_HOME")
    if env_home:
        candidate = Path(env_home)
        if candidate.is_dir():
            return candidate

    repo = get_repo_root()
    if (repo / ".jvis").is_dir():
        return repo

    # Installed package data
    pkg_data = _PKG_ROOT / "data"
    if pkg_data.is_dir():
        return pkg_data

    return repo


def get_data_dir() -> Path:
    """Return the path to bundled package data (src/jvis/data/).

    In development mode this is the literal ``src/jvis/data/`` directory.
    In installed mode it lives inside the wheel at ``jvis/data/``.
    """
    pkg_data = _PKG_ROOT / "data"
    if pkg_data.is_dir():
        return pkg_data

    # Fallback: treat JVIS_HOME as the data root (dev mode)
    return get_jvis_home()


def get_version_file() -> Path:
    """Return path to the .jvis/version file."""
    return get_jvis_home() / ".jvis" / "version"


def get_templates_dir() -> Path:
    """Return path to the templates/ directory.

    In the installed wheel the templates live under ``data/templates/``.
    In dev mode they live under ``<repo>/.jvis/templates/``.
    """
    # Installed package: src/jvis/data/templates/
    pkg_templates = get_data_dir() / "templates"
    if pkg_templates.is_dir():
        return pkg_templates

    # Dev mode fallback
    return get_jvis_home() / ".jvis" / "templates"

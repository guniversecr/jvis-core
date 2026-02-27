"""JVIS configuration loading."""

from __future__ import annotations

import logging
from importlib.metadata import PackageNotFoundError, version

from jvis.utils.paths import get_version_file

logger = logging.getLogger(__name__)


def read_version() -> str:
    """Read the JVIS version.

    Tries .jvis/version first (SSOT per ADR-001), falls back to
    importlib.metadata for pip-installed (non-dev) usage.
    """
    # 1. Repo file (dev mode / cloned repo) — SSOT per ADR-001
    version_file = get_version_file()
    try:
        file_version = version_file.read_text().strip()
        if file_version:
            return file_version
    except (FileNotFoundError, OSError):
        pass

    # 2. Installed package (pip install jvis)
    try:
        return version("jvis")
    except PackageNotFoundError:
        return "0.0.0"

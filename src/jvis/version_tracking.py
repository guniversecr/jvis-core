"""Version provenance tracking for JVIS target projects.

Stamps the JVIS version, install source, and timestamp into target
project config so ``jvis update`` can detect staleness.
"""

from __future__ import annotations

import logging
import re
from datetime import datetime, timezone
from pathlib import Path

logger = logging.getLogger(__name__)

_PROVENANCE_SECTION = "# --- JVIS Provenance (auto-managed, do not edit) ---"
_PROVENANCE_KEYS = ("jvis_installed_version", "jvis_source", "jvis_installed_at")


def stamp_version(target: Path, version: str, source: str) -> None:
    """Write version provenance into the target project's core-config.yaml.

    Uses text manipulation (not yaml.dump) to preserve comments.
    If provenance keys already exist, replaces them; otherwise appends a
    marked section at the end of the file.
    """
    config_path = target / ".jvis" / "core-config.yaml"
    if not config_path.is_file():
        logger.warning("core-config.yaml not found at %s, skipping stamp", config_path)
        return

    content = config_path.read_text()
    timestamp = datetime.now(tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    new_lines = [
        f'jvis_installed_version: "{version}"',
        f'jvis_source: "{source}"',
        f'jvis_installed_at: "{timestamp}"',
    ]

    # Check if provenance section already exists
    if _PROVENANCE_SECTION in content:
        # Replace entire provenance block
        pattern = re.escape(_PROVENANCE_SECTION) + r"\n(?:jvis_\w+:.*\n?)+"
        replacement = _PROVENANCE_SECTION + "\n" + "\n".join(new_lines) + "\n"
        content = re.sub(pattern, replacement, content)
    elif any(f"{key}:" in content for key in _PROVENANCE_KEYS):
        # Keys exist without section header — replace each individually
        for key, line in zip(_PROVENANCE_KEYS, new_lines):
            content = re.sub(rf"^{key}:.*$", line, content, flags=re.MULTILINE)
    else:
        # Append new section
        if not content.endswith("\n"):
            content += "\n"
        content += f"\n{_PROVENANCE_SECTION}\n" + "\n".join(new_lines) + "\n"

    config_path.write_text(content)
    logger.info("Stamped version %s (%s) into %s", version, source, config_path)


def read_provenance(target: Path) -> dict[str, str]:
    """Read version provenance from a target project's core-config.yaml.

    Returns a dict with keys ``jvis_installed_version``, ``jvis_source``,
    ``jvis_installed_at``.  Missing keys are omitted.
    """
    config_path = target / ".jvis" / "core-config.yaml"
    result: dict[str, str] = {}
    if not config_path.is_file():
        return result

    content = config_path.read_text()
    for key in _PROVENANCE_KEYS:
        match = re.search(rf'^{key}:\s*"?([^"\n]+)"?\s*$', content, re.MULTILINE)
        if match:
            result[key] = match.group(1).strip()

    return result


def detect_source_mode() -> str:
    """Return ``"dev"`` if running from a git checkout, ``"pip"`` if installed.

    Editable installs (``pip install -e .``) register with importlib.metadata
    but should still be treated as ``"dev"`` since the code lives in a repo.
    """
    from importlib.metadata import PackageNotFoundError
    from importlib.metadata import version as _meta_version
    from pathlib import Path

    try:
        _meta_version("jvis")
    except PackageNotFoundError:
        return "dev"

    # Editable install: the source tree contains a .git directory
    repo_root = Path(__file__).resolve().parent.parent.parent
    if (repo_root / ".git").is_dir():
        return "dev"

    return "pip"

"""Project name validation and path safety checks."""

from __future__ import annotations

import logging
import re
from pathlib import Path

logger = logging.getLogger(__name__)

# Valid project name: 2-64 chars, lowercase alphanumeric + hyphens/underscores.
# Must start with a letter (prevents names like "-foo" breaking shell commands).
# 64-char max aligns with DNS label limit (RFC 1035) — project names often become
# Docker container names, hostnames, and database names which share this constraint.
_NAME_RE = re.compile(r"^[a-z][a-z0-9_-]{1,63}$")

# System directories that must never be scaffold targets.
# Writing project files here would corrupt the OS or overwrite system binaries.
# Covers Linux FHS paths (/bin, /etc, /var, /proc, /sys, /boot, /run) and
# macOS-specific paths (/System, /Library, /Applications).
_FORBIDDEN_PATHS = frozenset(
    {
        "/",
        "/bin",
        "/sbin",
        "/usr",
        "/etc",
        "/var",
        "/tmp",
        "/root",
        "/home",
        "/System",
        "/Library",
        "/Applications",
        "/proc",
        "/dev",
        "/sys",
        "/boot",
        "/run",
    }
)


def sanitize_project_name(raw: str) -> str:
    """Normalize a raw name into a valid project name.

    Lowercases, replaces spaces/dots with hyphens, strips leading/trailing hyphens.
    """
    name = raw.strip().lower()
    name = re.sub(r"[\s.]+", "-", name)
    name = re.sub(r"[^a-z0-9_-]", "", name)
    name = name.strip("-_")
    return name


def validate_project_name(name: str) -> str | None:
    """Return *None* if *name* is valid, or an error message."""
    if not name:
        return "Project name cannot be empty."
    if not _NAME_RE.match(name):
        return (
            "Project name must start with a letter, be 2-64 characters, "
            "and contain only lowercase letters, digits, hyphens, or underscores."
        )
    return None


def validate_safe_path(path: Path) -> str | None:
    """Return *None* if *path* is safe to write to, or an error message."""
    raw = str(path)

    # Block directory traversal (CWE-22) — prevents "../../../etc/passwd" style attacks.
    if ".." in raw:
        return "Path contains '..' (directory traversal not allowed)."

    # Check both literal and resolved path to catch symlink-based bypasses.
    resolved = str(path.resolve())
    for check in (raw, resolved):
        if check in _FORBIDDEN_PATHS:
            return f"Cannot operate on system directory: {check}"

    if path.is_symlink():
        real = path.resolve()
        if str(real) in _FORBIDDEN_PATHS:
            return f"Symlink resolves to forbidden path: {real}"

    return None


# Maximum allowed project description length (CWE-400: Uncontrolled Resource Consumption).
_MAX_DESCRIPTION_LENGTH = 512


def validate_description(description: str) -> str | None:
    """Return *None* if *description* is valid, or an error message."""
    if len(description) > _MAX_DESCRIPTION_LENGTH:
        return f"Description too long ({len(description)} chars). Maximum is {_MAX_DESCRIPTION_LENGTH}."
    return None

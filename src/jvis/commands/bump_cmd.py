"""``jvis bump`` command — increment the project version across all version files."""

from __future__ import annotations

import logging
import re
from datetime import datetime, timezone
from pathlib import Path

import click

from jvis.utils import ui
from jvis.utils.paths import get_repo_root

logger = logging.getLogger(__name__)


def _bump_semver(current: str, part: str) -> str:
    """Compute the next semantic version."""
    match = re.match(r"^(\d+)\.(\d+)\.(\d+)", current)
    if not match:
        msg = f"Cannot parse version '{current}' as semver"
        raise click.ClickException(msg)

    major, minor, patch = int(match.group(1)), int(match.group(2)), int(match.group(3))
    if part == "major":
        return f"{major + 1}.0.0"
    if part == "minor":
        return f"{major}.{minor + 1}.0"
    return f"{major}.{minor}.{patch + 1}"


def _update_pyproject(root: Path, old: str, new: str, *, dry_run: bool) -> None:
    """Update version in pyproject.toml."""
    path = root / "pyproject.toml"
    if not path.is_file():
        return
    content = path.read_text()
    updated = re.sub(
        rf'^(version\s*=\s*"){re.escape(old)}"',
        rf'\g<1>{new}"',
        content,
        count=1,
        flags=re.MULTILINE,
    )
    if updated == content:
        click.echo(f"  {ui.yellow('Warning:')} version not found in pyproject.toml")
        return
    if not dry_run:
        path.write_text(updated)
    click.echo(f"  pyproject.toml: {old} -> {new}")


def _update_version_file(root: Path, new: str, *, dry_run: bool) -> None:
    """Overwrite .jvis/version."""
    path = root / ".jvis" / "version"
    if not path.is_file():
        return
    if not dry_run:
        path.write_text(f"{new}\n")
    click.echo(f"  .jvis/version:  {new}")


def _update_version_yaml(root: Path, old: str, new: str, *, dry_run: bool) -> None:
    """Update version, release_date, and component versions in .jvis/VERSION.yaml."""
    path = root / ".jvis" / "VERSION.yaml"
    if not path.is_file():
        return
    content = path.read_text()
    today = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d")

    # Replace top-level version line
    content = re.sub(
        rf"^(version:\s*){re.escape(old)}",
        rf"\g<1>{new}",
        content,
        count=1,
        flags=re.MULTILINE,
    )
    # Replace release_date line
    content = re.sub(
        r'^(release_date:\s*)"?\d{4}-\d{2}-\d{2}"?',
        rf'\g<1>"{today}"',
        content,
        count=1,
        flags=re.MULTILINE,
    )
    # Sync all component versions to the new version
    content = re.sub(
        r"^(\s+\w+:\s*)\d+\.\d+\.\d+",
        rf"\g<1>{new}",
        content,
        flags=re.MULTILINE,
    )
    if not dry_run:
        path.write_text(content)
    click.echo(f"  VERSION.yaml:   {old} -> {new} (date: {today})")


@click.command()
@click.argument("part", type=click.Choice(["patch", "minor", "major"]))
@click.option("--dry-run", is_flag=True, help="Show what would change without modifying files.")
def bump(part: str, dry_run: bool) -> None:
    """Bump the JVIS version (patch, minor, or major).

    Updates pyproject.toml, .jvis/version, and .jvis/VERSION.yaml.
    """
    from jvis.utils.config import read_version

    current = read_version()
    new = _bump_semver(current, part)

    click.echo(ui.header("JVIS Version Bump"))
    click.echo(f"  Current: {current}")
    click.echo(f"  New:     {new}  ({part})")
    click.echo("")

    root = get_repo_root()

    if dry_run:
        click.echo("  Dry run — showing changes:")
        click.echo("")

    _update_pyproject(root, current, new, dry_run=dry_run)
    _update_version_file(root, new, dry_run=dry_run)
    _update_version_yaml(root, current, new, dry_run=dry_run)

    if dry_run:
        click.echo(f"\n  {ui.yellow('No files modified.')}")
    else:
        click.echo(f"\n  {ui.green('Version bumped to')} {new}")
        click.echo("  Remember to update CHANGELOG.md before releasing.")

"""Collect project name, description, and location from the user."""

from __future__ import annotations

import logging
from pathlib import Path

import click

from jvis.utils import ui
from jvis.utils.fs import is_writable, mkdir_p
from jvis.utils.validation import sanitize_project_name, validate_description, validate_project_name, validate_safe_path

logger = logging.getLogger(__name__)


def collect_project_info() -> tuple[str, str, Path]:
    """Prompt for project name, description, and directory. Returns (name, description, path)."""
    name = _prompt_name()
    description = _prompt_description()
    project_dir = _prompt_location(name)
    return name, description, project_dir


def _prompt_name() -> str:
    while True:
        raw = click.prompt(ui.cyan("Project name"), type=str)
        name = sanitize_project_name(raw)
        err = validate_project_name(name)
        if err is None:
            click.echo(f"  {ui.green('✓')} Name: {ui.bold(name)}")
            return name
        click.echo(f"  {ui.red('✗')} {err}")
        if name != raw.strip():
            click.echo(f"    Sanitized to: {name!r}")


def _prompt_description() -> str:
    while True:
        result: str = click.prompt(ui.cyan("Brief description"), default="", show_default=False)
        err = validate_description(result)
        if err is None:
            return result
        click.echo(f"  {ui.red('✗')} {err}")


def _prompt_location(project_name: str) -> Path:
    default_base = Path.home() / "Projects"
    cwd = Path.cwd()

    click.echo("")
    click.echo("  Location options:")
    click.echo(f"    1) Current directory: {cwd}")
    click.echo(f"    2) Projects directory: {default_base / project_name}")
    click.echo("    3) Custom path")
    click.echo("")

    while True:
        choice = click.prompt("  Select", default="2", show_default=True)

        if choice == "1":
            project_dir = cwd
        elif choice == "2":
            project_dir = default_base / project_name
        elif choice == "3":
            custom = click.prompt("  Enter path", type=str)
            project_dir = Path(custom).expanduser().resolve()
            # If path doesn't end with project name, ask
            if project_dir.name != project_name and click.confirm(
                f"  Create '{project_name}' inside {project_dir}?", default=True
            ):
                project_dir = project_dir / project_name
        else:
            click.echo(f"  {ui.red('Invalid option')}. Select 1, 2, or 3.")
            continue

        # Validate path safety
        err = validate_safe_path(project_dir)
        if err:
            click.echo(f"  {ui.red('✗')} {err}")
            continue

        # Check parent is writable
        parent = project_dir.parent
        if parent.exists() and not is_writable(parent):
            click.echo(f"  {ui.red('✗')} No write permission: {parent}")
            continue

        # Create parent if needed
        if not parent.exists():
            try:
                mkdir_p(parent)
            except PermissionError:
                click.echo(f"  {ui.red('✗')} Cannot create: {parent}")
                continue

        click.echo(f"  {ui.green('✓')} Location: {project_dir}")
        return project_dir

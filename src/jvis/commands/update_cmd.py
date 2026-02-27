"""``jvis update`` command — update JVIS in an existing project."""

from __future__ import annotations

import logging
from pathlib import Path

import click

from jvis.utils import ui

logger = logging.getLogger(__name__)


@click.command()
@click.argument("path", default=".")
@click.option("--yes", "-y", is_flag=True, help="Skip confirmation prompt.")
@click.option("--dry-run", is_flag=True, help="Show what would change without modifying files.")
def update(path: str, yes: bool, dry_run: bool) -> None:
    """Update JVIS framework in an existing project.

    PATH defaults to the current directory.
    """
    from jvis.detection.project_state import detect_project_state, get_jvis_version
    from jvis.utils.config import read_version
    from jvis.version_tracking import detect_source_mode, read_provenance

    target = Path(path).resolve()

    click.echo(ui.header("JVIS Update"))

    # 1. Validate target
    state = detect_project_state(target)
    if state not in ("has_context", "has_aicore"):
        raise click.ClickException(f"No JVIS installation found at {target}. Use 'jvis new' or 'jvis add' first.")

    # 2. Compare versions
    source_version = read_version()
    installed_version = get_jvis_version(target)
    provenance = read_provenance(target)
    installed_display = provenance.get("jvis_installed_version", installed_version)

    click.echo(f"  Installed: {installed_display}")
    click.echo(f"  Available: {source_version}")

    if installed_display == source_version:
        click.echo(f"\n  {ui.green('Already up to date.')} (v{source_version})")
        return

    # 3. Show what will be updated
    click.echo("")
    click.echo("  Will update:")
    click.echo("    .jvis/agents/          (agent configs)")
    click.echo("    .jvis/tasks/           (task workflows)")
    click.echo("    .jvis/templates/       (document templates)")
    click.echo("    .jvis/agent-engine/    (generator)")
    click.echo("    .claude/commands/      (slash commands)")
    click.echo("    .claude/skills/        (domain knowledge)")
    click.echo("")
    click.echo("  Will preserve:")
    click.echo("    docs/notes/            (agent handoff notes)")
    click.echo("    docs/plans/            (execution plans)")
    click.echo("    .jvis/core-config.yaml (project config)")

    if dry_run:
        click.echo(f"\n  {ui.yellow('Dry run — no changes made.')}")
        return

    # 4. Confirm
    if not yes:
        click.echo("")
        if not click.confirm(f"  Update {installed_display} -> {source_version}?", default=True):
            click.echo(f"  {ui.yellow('Cancelled.')}")
            raise click.exceptions.Exit(0)

    # 5. Run update
    from jvis.scaffold.framework import install_framework
    from jvis.version_tracking import stamp_version

    click.echo("")
    click.echo(ui.cyan("  Updating JVIS framework..."))
    install_framework(target)

    source = detect_source_mode()
    stamp_version(target, source_version, source)

    click.echo("")
    click.echo(f"  {ui.green('Updated successfully.')} v{installed_display} -> v{source_version}")

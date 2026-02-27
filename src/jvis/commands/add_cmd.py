"""``jvis add`` command — add JVIS to an existing project."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import TYPE_CHECKING

import click

if TYPE_CHECKING:
    from jvis.detection.tech_stack import StackDetection

from jvis.utils import ui

logger = logging.getLogger(__name__)


@click.command()
@click.argument("path")
@click.option("--yes", "-y", is_flag=True, help="Skip confirmation prompts.")
@click.option("--entity", "-e", default="item", help="Domain entity name (singular, e.g. product, task, user).")
def add(path: str, yes: bool, entity: str) -> None:
    """Add JVIS to an existing project at PATH."""
    from jvis.detection.project_state import detect_project_state
    from jvis.detection.tech_stack import detect_project_type, detect_tech_stack
    from jvis.utils.validation import validate_safe_path

    target = Path(path).resolve()

    click.echo(ui.header("JVIS — Add to Existing Project"))

    if not target.is_dir():
        raise click.ClickException(f"Directory does not exist: {target}")

    err = validate_safe_path(target)
    if err:
        raise click.ClickException(err)

    click.echo(f"  Project: {target}")

    # Analyze project
    click.echo("")
    click.echo(ui.cyan("  Analyzing project..."))

    state = detect_project_state(target)
    detection = detect_tech_stack(target)
    project_type = detect_project_type(target)

    click.echo(f"  State:   {state}")
    click.echo(f"  Type:    {project_type}")
    if detection.summary != "unknown":
        click.echo(f"  Stack:   {detection.summary}")
    if detection.recommended_agents:
        click.echo(f"  Agents:  {', '.join(detection.recommended_agents)}")

    # Handle existing JVIS installations
    if not _confirm_existing_install(state, yes):
        raise click.exceptions.Exit(0)

    # Confirm
    if not yes:
        click.echo("")
        if not click.confirm("  Continue with installation?", default=True):
            click.echo(f"  {ui.yellow('Cancelled.')}")
            raise click.exceptions.Exit(0)

    # Install
    _install_jvis(target, state, detection)


def _confirm_existing_install(state: str, yes: bool) -> bool:
    """Handle confirmation for existing JVIS installations. Returns True to proceed."""
    if state == "has_context":
        click.echo(f"\n  {ui.yellow('⚠')} JVIS already installed with active context.")
        click.echo("  Use 'jvis update' to update, or reinstall below.")
        if not yes and not click.confirm("  Reinstall JVIS? (framework files will be overwritten)", default=False):
            return False
    elif state == "has_aicore":
        click.echo(f"\n  {ui.yellow('⚠')} JVIS already installed.")
        if not yes and not click.confirm("  Reinstall?", default=False):
            return False
    elif state == "has_code":
        click.echo("\n  Brownfield project detected. JVIS will be added preserving existing code.")
    elif state == "empty":
        click.echo("\n  Empty directory — standard installation.")

    return True


def _install_jvis(target: Path, state: str, detection: StackDetection) -> None:
    """Run the actual JVIS installation into target directory."""
    from jvis.scaffold.docs_structure import create_context_map, create_docs_structure
    from jvis.scaffold.framework import install_framework
    from jvis.scaffold.shared_files import create_shared_files
    from jvis.utils.git import setup_git

    click.echo("")
    click.echo(ui.cyan("  Installing JVIS..."))

    project_name = target.name

    click.echo("  Installing JVIS framework...")
    install_framework(target)

    from jvis.utils.config import read_version
    from jvis.version_tracking import detect_source_mode, stamp_version

    stamp_version(target, read_version(), detect_source_mode())

    click.echo("  Creating documentation structure...")
    create_docs_structure(target)

    click.echo("  Generating context map...")
    primary_lang = detection.languages[0] if detection.languages else "unknown"
    primary_fw = detection.frameworks[0] if detection.frameworks else "custom"
    primary_db = detection.databases[0] if detection.databases else "none"
    create_context_map(
        project_path=target,
        stack=primary_fw,
        database=primary_db,
        language=primary_lang,
    )

    if not (target / "README.md").exists():
        click.echo("  Creating shared files...")
        create_shared_files(target, project_name)

    click.echo("  Configuring git...")
    primary_stack = detection.frameworks[0] if detection.frameworks else ""
    setup_git(target, primary_stack)

    # Summary
    click.echo("")
    click.echo(ui.header("JVIS Added Successfully"))
    click.echo(f"  {ui.green('✓')} JVIS installed in: {target}")
    click.echo("")
    click.echo("  Next steps:")
    click.echo(f"    cd {target}")
    click.echo("    claude")
    click.echo("")
    if state == "has_code":
        click.echo("  For brownfield projects:")
        click.echo("    /architect")
        click.echo("    *document-project")
        click.echo("")

"""``jvis new`` command — create a new JVIS project, implemented in pure Python."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

import click

if TYPE_CHECKING:
    from jvis.stacks.registry import StackInfo

from jvis.utils import ui

logger = logging.getLogger(__name__)


@dataclass
class ProjectConfig:
    """All settings needed to scaffold a new JVIS project."""

    project_name: str
    project_description: str
    project_dir: Path
    project_type: str
    stacks: dict[str, StackInfo | None]
    database: str
    entity_name: str = "item"


@click.command()
@click.option("--name", "-n", default=None, help="Project name (skips interactive prompt).")
@click.option(
    "--stack",
    "-s",
    default=None,
    help="Stack id (e.g. python-fastapi, python-django, nodejs-nestjs, react-vite, angular, nextjs, custom).",
)
@click.option("--path", "-p", "dest_path", default=None, help="Target directory for the project.")
@click.option("--database", "-d", "db", default=None, help="Database: postgresql, mysql, dynamodb.")
@click.option("--yes", "-y", is_flag=True, help="Skip confirmation prompt.")
@click.option("--entity", "-e", default="item", help="Domain entity name (singular, e.g. product, task, user).")
def new(name: str | None, stack: str | None, dest_path: str | None, db: str | None, yes: bool, entity: str) -> None:
    """Create a new JVIS project.

    Interactive by default. Use flags for scripted usage:

        jvis new --name my-api --stack python-fastapi --path ./my-api -y
    """
    from jvis.core.summary import show_summary_and_confirm

    click.echo(ui.header("JVIS Project Initializer"))

    if name and stack and dest_path:
        config = _collect_config_scripted(name, stack, dest_path, db, entity)
    else:
        config = _collect_config_interactive(entity)

    if not yes and not show_summary_and_confirm(
        config.project_name,
        config.project_description,
        config.project_dir,
        config.project_type,
        config.stacks,
        config.database,
    ):
        click.echo(f"\n  {ui.yellow('Cancelled.')}")
        raise click.exceptions.Exit(0)

    _scaffold_project(config)
    _print_post_install(config)


def _collect_config_scripted(
    name: str,
    stack_id: str,
    dest_path: str,
    db: str | None,
    entity: str = "item",
) -> ProjectConfig:
    """Validate CLI flags and build config for scripted (non-interactive) flow."""
    from jvis.core.database_selector import DATABASES
    from jvis.stacks.registry import get_stack
    from jvis.utils.validation import sanitize_project_name, validate_project_name, validate_safe_path

    project_name = sanitize_project_name(name)
    err = validate_project_name(project_name)
    if err:
        raise click.ClickException(err)

    project_dir = Path(dest_path).expanduser().resolve()
    err = validate_safe_path(project_dir)
    if err:
        raise click.ClickException(err)

    stack_info = get_stack(stack_id)
    if stack_info is None:
        from jvis.stacks.registry import discover_stacks

        available = ", ".join(sorted(discover_stacks().keys()))
        raise click.ClickException(f"Unknown stack '{stack_id}'. Available: {available}.")

    stacks: dict[str, StackInfo | None] = {
        "stack": stack_info,
        "backend": None,
        "frontend": None,
        "mobile": None,
    }

    valid_dbs = {d[0] for d in DATABASES}
    if db and db not in valid_dbs:
        raise click.ClickException(f"Unknown database '{db}'. Available: {', '.join(valid_dbs)}.")
    database = ""
    if stack_info.requires_database:
        database = db or "postgresql"

    entity_name = _validate_entity(entity)

    return ProjectConfig(
        project_name=project_name,
        project_description="",
        project_dir=project_dir,
        project_type="single",
        stacks=stacks,
        database=database,
        entity_name=entity_name,
    )


def _collect_config_interactive(entity: str = "item") -> ProjectConfig:
    """Run interactive prompts to build project config."""
    from jvis.core.database_selector import select_database
    from jvis.core.project_info import collect_project_info
    from jvis.core.project_type import select_project_type
    from jvis.core.stack_selector import select_stacks_for_type

    project_name, project_description, project_dir = collect_project_info()
    project_type = select_project_type()
    stacks = select_stacks_for_type(project_type)
    db_stack = stacks.get("backend") or stacks.get("stack")
    database = select_database(db_stack)

    entity_name = _validate_entity(entity)

    return ProjectConfig(
        project_name=project_name,
        project_description=project_description,
        project_dir=project_dir,
        project_type=project_type,
        stacks=stacks,
        database=database,
        entity_name=entity_name,
    )


def _validate_entity(entity: str) -> str:
    """Validate and normalize entity name. Returns lowercase entity."""
    import re

    entity = entity.strip().lower()
    if not entity or len(entity) < 2:
        raise click.ClickException("Entity name must be at least 2 characters.")
    if not re.match(r"^[a-z]{2,30}$", entity):
        raise click.ClickException("Entity name must be a single word, lowercase letters only (2-30 chars).")
    return entity


def _scaffold_project(config: ProjectConfig) -> None:
    """Create all project files — stacks, framework, docs, git."""
    from jvis.scaffold.docs_structure import create_context_map, create_docs_structure
    from jvis.scaffold.entity_rename import apply_entity_name
    from jvis.scaffold.framework import install_framework
    from jvis.scaffold.shared_files import create_shared_files
    from jvis.utils.git import setup_git

    click.echo("")
    click.echo(ui.cyan("  Creating project..."))
    config.project_dir.mkdir(parents=True, exist_ok=True)

    if config.project_type == "single":
        _scaffold_single_stack(config)
    else:
        _scaffold_monorepo(config)

    if config.entity_name != "item":
        click.echo(f"  Applying entity name '{config.entity_name}'...")
        apply_entity_name(config.project_dir, config.entity_name)

    click.echo("  Installing JVIS framework...")
    install_framework(config.project_dir)

    from jvis.utils.config import read_version
    from jvis.version_tracking import detect_source_mode, stamp_version

    stamp_version(config.project_dir, read_version(), detect_source_mode())

    click.echo("  Creating documentation structure...")
    create_docs_structure(config.project_dir)

    primary_stack = config.stacks.get("stack") or config.stacks.get("backend")

    click.echo("  Generating context map...")
    create_context_map(
        project_path=config.project_dir,
        stack=primary_stack.id if primary_stack else "custom",
        database=config.database or "none",
        language=primary_stack.language if primary_stack else "unknown",
    )

    click.echo("  Creating shared files...")
    create_shared_files(config.project_dir, config.project_name, config.project_description, primary_stack)

    click.echo("  Initializing git...")
    setup_git(config.project_dir, primary_stack.id if primary_stack else "")


def _scaffold_single_stack(config: ProjectConfig) -> None:
    """Create a single-stack project structure."""
    from jvis.scaffold.stack_runner import run_stack

    stack = config.stacks.get("stack")
    if stack and stack.directory:
        click.echo(f"  Creating {stack.name} structure...")
        run_stack(stack, config.project_dir, config.project_name, config.project_description, config.database)


def _scaffold_monorepo(config: ProjectConfig) -> None:
    """Create a monorepo project structure with backend/frontend/mobile."""
    from jvis.scaffold.monorepo import create_monorepo_root
    from jvis.scaffold.stack_runner import run_stack

    backend = config.stacks.get("backend")
    frontend = config.stacks.get("frontend")
    mobile = config.stacks.get("mobile")

    click.echo("  Creating monorepo structure...")
    create_monorepo_root(config.project_dir, config.project_name, backend, frontend, config.database, mobile)

    if backend and backend.directory:
        click.echo(f"  Creating backend ({backend.name})...")
        run_stack(
            backend, config.project_dir / "server", config.project_name, config.project_description, config.database
        )

    if frontend and frontend.directory:
        click.echo(f"  Creating frontend ({frontend.name})...")
        run_stack(
            frontend, config.project_dir / "client", config.project_name, config.project_description, config.database
        )


def _print_post_install(config: ProjectConfig) -> None:
    """Print post-creation summary, setup hints, and recommended workflow."""
    primary_stack = config.stacks.get("stack") or config.stacks.get("backend")

    click.echo("")
    click.echo(ui.header("Project Created"))
    click.echo(f"  {ui.green('✓')} {ui.bold(config.project_name)} created at:")
    click.echo(f"    {config.project_dir}")
    click.echo("")
    click.echo("  Next steps:")
    click.echo(f"    cd {config.project_dir}")
    click.echo("")

    _print_setup_hints(primary_stack)

    click.echo("")
    click.echo("  Start AI-assisted development:")
    click.echo("    claude")
    click.echo("")
    click.echo("  Recommended workflow:")
    click.echo("    /pm         → Create PRD")
    click.echo("    /architect  → Design architecture")
    click.echo("    /sm         → Create stories")
    click.echo("    /dev        → Implement")
    click.echo("    /qa         → Review & quality gates")
    click.echo("")
    click.echo("  New to JVIS?")
    click.echo("    See docs/QUICKSTART.md or docs/manuals/tutorials/")
    click.echo("")


def _print_setup_hints(stack: StackInfo | None) -> None:
    """Print setup hints from stack manifest data."""
    if not stack or not stack.getting_started:
        return

    gs = stack.getting_started
    prerequisites = gs.get("prerequisites", "")
    commands: list[str] = gs.get("commands", [])

    if prerequisites:
        click.echo(f"  Setup ({prerequisites} required):")
    elif commands:
        click.echo("  Setup:")
    else:
        return

    for cmd in commands:
        click.echo(f"    {cmd}")

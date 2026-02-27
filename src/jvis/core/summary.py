"""Show a summary table and ask for confirmation before creating the project."""

from __future__ import annotations

import logging
from pathlib import Path

import click

from jvis.stacks.registry import StackInfo
from jvis.utils import ui

logger = logging.getLogger(__name__)


def show_summary_and_confirm(
    project_name: str,
    project_description: str,
    project_dir: Path,
    project_type: str,
    stacks: dict[str, StackInfo | None],
    database: str,
) -> bool:
    """Display a summary table and return True if user confirms."""
    click.echo("")
    click.echo(ui.header("Project Summary"))

    rows: list[tuple[str, str]] = []
    rows.append(("Project", project_name))

    if project_description:
        rows.append(("Description", project_description))

    type_labels = {
        "single": "Single-Stack",
        "fullstack": "Full-Stack",
        "fullstack-mobile": "Full-Stack + Mobile",
        "saas-platform": "SaaS Platform",
    }
    rows.append(("Type", type_labels.get(project_type, project_type)))

    if stacks.get("stack"):
        rows.append(("Stack", stacks["stack"].name))  # type: ignore[union-attr]
    if stacks.get("backend"):
        rows.append(("Backend", f"{stacks['backend'].name} → server/"))  # type: ignore[union-attr]
    if stacks.get("frontend"):
        rows.append(("Frontend", f"{stacks['frontend'].name} → client/"))  # type: ignore[union-attr]
    if stacks.get("mobile"):
        rows.append(("Mobile", f"{stacks['mobile'].name} → mobile/"))  # type: ignore[union-attr]
    if database:
        rows.append(("Database", database))

    rows.append(("Location", str(project_dir)))

    # Render table
    max_label = max(len(r[0]) for r in rows)
    for label, value in rows:
        click.echo(f"  {ui.cyan(label.ljust(max_label))}  {value}")

    click.echo("")
    return click.confirm(f"  {ui.bold('Create project?')}", default=True)

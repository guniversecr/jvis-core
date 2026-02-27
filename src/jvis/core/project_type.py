"""Select project type: single, fullstack, fullstack-mobile, saas-platform."""

from __future__ import annotations

import logging

import click

from jvis.utils import ui

logger = logging.getLogger(__name__)

PROJECT_TYPES = [
    ("single", "Single-Stack", "One stack (backend, frontend, or mobile)"),
    ("fullstack", "Full-Stack", "Backend + Frontend Web (server/ + client/)"),
    ("fullstack-mobile", "Full-Stack + Mobile", "Backend + Frontend + Mobile App"),
    ("saas-platform", "SaaS Platform", "Multi-tenant platform (server/ + client/ + infra/)"),
]


def select_project_type() -> str:
    """Prompt user to pick a project type. Returns the type id."""
    click.echo("")
    click.echo(ui.cyan("  Project type:"))
    click.echo("")
    for i, (_, label, desc) in enumerate(PROJECT_TYPES, 1):
        click.echo(f"    {i}) {ui.bold(label)}")
        click.echo(f"       {desc}")
        click.echo("")

    while True:
        choice = click.prompt("  Select type", default="1", show_default=True)
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(PROJECT_TYPES):
                type_id, label, _ = PROJECT_TYPES[idx]
                click.echo(f"  {ui.green('✓')} Type: {label}")
                return type_id
        except ValueError:
            pass
        click.echo(f"  {ui.red('Invalid')}. Enter 1-{len(PROJECT_TYPES)}.")

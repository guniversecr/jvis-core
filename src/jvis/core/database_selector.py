"""Database selection for backend stacks."""

from __future__ import annotations

import logging

import click

from jvis.stacks.registry import StackInfo
from jvis.utils import ui

logger = logging.getLogger(__name__)

# Supported databases ordered by recommendation. PostgreSQL first because it's the
# most feature-complete open-source RDBMS (JSON, full-text search, extensions).
DATABASES = [
    ("postgresql", "PostgreSQL", "Robust relational database (recommended)"),
    ("mysql", "MySQL / MariaDB", "Popular relational database"),
    ("dynamodb", "DynamoDB", "AWS NoSQL database"),
]


def select_database(stack: StackInfo | None) -> str:
    """Prompt for database selection if the stack requires it. Returns db id or ""."""
    if stack is None or not stack.requires_database:
        return ""

    click.echo("")
    click.echo(f"  {ui.cyan('Select database:')}")
    for i, (_, name, desc) in enumerate(DATABASES, 1):
        click.echo(f"    {i}) {ui.bold(name)} — {desc}")
    click.echo("")

    while True:
        choice = click.prompt("  Select database", default="1", show_default=True)
        try:
            # Users see 1-indexed menu; convert to 0-indexed list access
            idx = int(choice) - 1
            if 0 <= idx < len(DATABASES):
                db_id, name, _ = DATABASES[idx]
                click.echo(f"  {ui.green('✓')} Database: {name}")
                return db_id
        except ValueError:
            pass
        click.echo(f"  {ui.red('Invalid')}. Enter 1-{len(DATABASES)}.")

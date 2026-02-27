"""JVIS CLI — Click-based command-line interface.

All commands are implemented in pure Python.
"""

from __future__ import annotations

import click

from jvis.commands.add_cmd import add
from jvis.commands.bump_cmd import bump
from jvis.commands.primary import new
from jvis.commands.update_cmd import update
from jvis.commands.utility import (
    hooks,
    pipeline,
    version_cmd,
)
from jvis.utils.config import read_version


@click.group(invoke_without_command=True)
@click.option("--verbose", "-v", is_flag=True, help="Enable debug logging.")
@click.version_option(version=read_version(), prog_name="JVIS Manager")
@click.pass_context
def cli(ctx: click.Context, *, verbose: bool) -> None:
    """JVIS — Journey Virtual Intelligent System."""
    from jvis.log_config import setup_logging

    setup_logging(verbose=verbose)
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


# Primary commands
cli.add_command(new)
cli.add_command(add)
cli.add_command(update)
cli.add_command(bump)

# Utility commands
cli.add_command(version_cmd)
cli.add_command(pipeline)
cli.add_command(hooks)


def main() -> None:
    """Entry point for the `jvis` console script."""
    cli()

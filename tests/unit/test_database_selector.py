"""Tests for jvis.core.database_selector."""

from __future__ import annotations

import click
from click.testing import CliRunner

from jvis.core.database_selector import DATABASES, select_database
from jvis.stacks.registry import StackInfo


def _make_stack(requires_db: bool = True) -> StackInfo:
    return StackInfo(
        id="test",
        name="Test",
        description="",
        type="backend",
        language="python",
        framework="flask",
        requires_database=requires_db,
    )


def _wrap_select(stack: StackInfo | None) -> click.BaseCommand:
    """Wrap select_database in a Click command for CliRunner testing."""

    @click.command()
    def cmd() -> None:
        result = select_database(stack)
        click.echo(f"RESULT:{result}")

    return cmd


class TestDatabaseSelector:
    def test_databases_list(self):
        """DATABASES has 3 entries."""
        assert len(DATABASES) == 3

    def test_no_database_when_none_stack(self):
        """Returns empty string when stack is None."""
        runner = CliRunner()
        result = runner.invoke(_wrap_select(None), input="")
        assert result.exit_code == 0
        assert "RESULT:" in result.output

    def test_no_database_when_not_required(self):
        """Returns empty string when stack doesn't require database."""
        stack = _make_stack(requires_db=False)
        runner = CliRunner()
        result = runner.invoke(_wrap_select(stack), input="")
        assert result.exit_code == 0
        assert "RESULT:" in result.output

    def test_select_postgresql_default(self):
        """Default selection (1) returns 'postgresql'."""
        stack = _make_stack()
        runner = CliRunner()
        result = runner.invoke(_wrap_select(stack), input="1\n")
        assert result.exit_code == 0
        assert "RESULT:postgresql" in result.output

    def test_select_mysql(self):
        """Selecting 2 returns 'mysql'."""
        stack = _make_stack()
        runner = CliRunner()
        result = runner.invoke(_wrap_select(stack), input="2\n")
        assert result.exit_code == 0
        assert "RESULT:mysql" in result.output

    def test_invalid_then_valid(self):
        """Invalid input re-prompts."""
        stack = _make_stack()
        runner = CliRunner()
        result = runner.invoke(_wrap_select(stack), input="0\n3\n")
        assert result.exit_code == 0
        assert "RESULT:dynamodb" in result.output

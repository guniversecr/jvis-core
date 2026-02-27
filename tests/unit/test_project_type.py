"""Tests for jvis.core.project_type."""

from __future__ import annotations

import click
from click.testing import CliRunner

from jvis.core.project_type import PROJECT_TYPES, select_project_type


def _wrap_select() -> click.BaseCommand:
    """Wrap select_project_type in a Click command for CliRunner testing."""

    @click.command()
    def cmd() -> None:
        result = select_project_type()
        click.echo(f"RESULT:{result}")

    return cmd


class TestProjectTypes:
    def test_project_types_list(self):
        """PROJECT_TYPES has 4 entries."""
        assert len(PROJECT_TYPES) == 4

    def test_project_types_ids(self):
        """All expected type IDs are present."""
        ids = {t[0] for t in PROJECT_TYPES}
        assert ids == {"single", "fullstack", "fullstack-mobile", "saas-platform"}

    def test_select_project_type_default(self):
        """Default selection (1) returns 'single'."""
        runner = CliRunner()
        result = runner.invoke(_wrap_select(), input="1\n")
        assert result.exit_code == 0
        assert "RESULT:single" in result.output

    def test_select_project_type_fullstack(self):
        """Selecting 2 returns 'fullstack'."""
        runner = CliRunner()
        result = runner.invoke(_wrap_select(), input="2\n")
        assert result.exit_code == 0
        assert "RESULT:fullstack" in result.output

    def test_select_project_type_invalid_then_valid(self):
        """Invalid input re-prompts."""
        runner = CliRunner()
        result = runner.invoke(_wrap_select(), input="99\n3\n")
        assert result.exit_code == 0
        assert "RESULT:fullstack-mobile" in result.output

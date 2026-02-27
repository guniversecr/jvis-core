"""Tests for the --verbose / -v CLI flag."""

from __future__ import annotations

import logging

from click.testing import CliRunner

from jvis.cli import cli


class TestVerboseFlag:
    """Verify the --verbose flag integrates with setup_logging."""

    def test_verbose_flag_accepted(self) -> None:
        runner = CliRunner()
        result = runner.invoke(cli, ["--verbose", "--help"])
        assert result.exit_code == 0
        assert "JVIS" in result.output

    def test_short_flag_accepted(self) -> None:
        runner = CliRunner()
        result = runner.invoke(cli, ["-v", "--help"])
        assert result.exit_code == 0

    def test_verbose_sets_debug_level(self) -> None:
        runner = CliRunner()
        # Invoke without --help so the function body (setup_logging) actually runs
        runner.invoke(cli, ["--verbose"])
        root = logging.getLogger("jvis")
        assert root.level == logging.DEBUG

    def test_default_sets_warning_level(self) -> None:
        runner = CliRunner()
        # Invoke without --help so setup_logging runs with verbose=False
        runner.invoke(cli, [])
        root = logging.getLogger("jvis")
        assert root.level == logging.WARNING

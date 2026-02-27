"""Tests for the JVIS Click CLI.

Tests pure-Python commands with Click's CliRunner.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from click.testing import CliRunner

from jvis.cli import cli


@pytest.fixture
def runner():
    return CliRunner()


# =============================================================================
# HELP & VERSION
# =============================================================================


class TestHelpAndVersion:
    def test_help_lists_all_registered_commands(self, runner):
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        for cmd in ("new", "add", "bump", "update", "pipeline", "hooks", "version"):
            assert cmd in result.output, f"Expected command '{cmd}' in help output"

    def test_version_flag(self, runner):
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "JVIS Manager" in result.output

    def test_version_command(self, runner):
        result = runner.invoke(cli, ["version"])
        assert result.exit_code == 0
        assert "JVIS Manager v" in result.output

    def test_no_args_shows_help(self, runner):
        result = runner.invoke(cli, [])
        assert result.exit_code == 0
        assert "Commands:" in result.output

    def test_unknown_command_errors(self, runner):
        result = runner.invoke(cli, ["nonexistent-cmd"])
        assert result.exit_code != 0


# =============================================================================
# PURE PYTHON COMMANDS
# =============================================================================


class TestRemovedCommands:
    def test_verticals_not_found(self, runner):
        result = runner.invoke(cli, ["verticals"])
        assert result.exit_code != 0

    def test_modules_not_found(self, runner):
        result = runner.invoke(cli, ["modules"])
        assert result.exit_code != 0

    def test_features_not_found(self, runner):
        result = runner.invoke(cli, ["features"])
        assert result.exit_code != 0


class TestPipeline:
    def test_pipeline_default_github(self, runner):
        result = runner.invoke(cli, ["pipeline"])
        assert result.exit_code == 0
        assert "CI/CD PIPELINE GENERATOR" in result.output
        assert "GitHub Actions" in result.output

    def test_pipeline_gitlab(self, runner):
        result = runner.invoke(cli, ["pipeline", "gitlab"])
        assert result.exit_code == 0
        assert "GitLab CI" in result.output

    def test_pipeline_azure(self, runner):
        result = runner.invoke(cli, ["pipeline", "azure"])
        assert result.exit_code == 0
        assert "Azure DevOps" in result.output

    def test_pipeline_unknown(self, runner):
        result = runner.invoke(cli, ["pipeline", "bitbucket"])
        assert result.exit_code == 0
        assert "not recognized" in result.output


class TestHooks:
    def test_hooks_output(self, runner):
        result = runner.invoke(cli, ["hooks"])
        assert result.exit_code == 0
        assert "Available JVIS Hooks" in result.output


# =============================================================================
# UI HELPERS TESTS
# =============================================================================


class TestUIHelpers:
    def test_header(self):
        from jvis.utils.ui import header

        h = header("TEST")
        assert "TEST" in h

    def test_error(self):
        from jvis.utils.ui import error

        e = error("something broke")
        assert "something broke" in e

    def test_colors_without_tty(self):
        from jvis.utils import ui

        # In test context, stdout is not a TTY, so colors may be disabled
        # Verify functions still return the text content
        assert "hello" in ui.red("hello")
        assert "hello" in ui.green("hello")
        assert "hello" in ui.cyan("hello")


# =============================================================================
# CONFIG TESTS
# =============================================================================


class TestConfig:
    def test_read_version(self):
        from jvis.utils.config import read_version

        version = read_version()
        version_file = Path(__file__).parent.parent.parent / ".jvis" / "version"
        expected = version_file.read_text().strip()
        assert version == expected

    def test_paths_resolution(self):
        import yaml

        from jvis.utils.paths import get_jvis_home

        home = get_jvis_home()
        assert home.is_dir()
        config_path = home / ".jvis" / "core-config.yaml"
        assert config_path.is_file()
        config = yaml.safe_load(config_path.read_text())
        assert isinstance(config, dict), "core-config.yaml must be a YAML mapping"
        assert "qa" in config, "core-config.yaml must contain qa section"

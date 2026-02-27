"""Tests for version management: bump, update, and provenance tracking."""

from __future__ import annotations

from pathlib import Path

import pytest
from click.testing import CliRunner

from jvis.cli import cli


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


@pytest.fixture
def tmp_project(tmp_path):
    """Create a minimal JVIS project directory for testing."""
    jvis_dir = tmp_path / ".jvis"
    jvis_dir.mkdir()
    (jvis_dir / "version").write_text("4.0.0\n")
    (jvis_dir / "core-config.yaml").write_text("markdownExploder: true\nqa:\n  qaLocation: docs/qa\n")
    return tmp_path


# =============================================================================
# BUMP COMMAND
# =============================================================================


class TestBumpCommand:
    def test_bump_dry_run(self, runner: CliRunner) -> None:
        result = runner.invoke(cli, ["bump", "patch", "--dry-run"])
        assert result.exit_code == 0
        assert "Dry run" in result.output or "No files modified" in result.output
        assert "4.5.4" in result.output

    def test_bump_patch_arithmetic(self) -> None:
        from jvis.commands.bump_cmd import _bump_semver

        assert _bump_semver("4.1.0", "patch") == "4.1.1"

    def test_bump_minor_arithmetic(self) -> None:
        from jvis.commands.bump_cmd import _bump_semver

        assert _bump_semver("4.1.0", "minor") == "4.2.0"

    def test_bump_major_arithmetic(self) -> None:
        from jvis.commands.bump_cmd import _bump_semver

        assert _bump_semver("4.1.0", "major") == "5.0.0"

    def test_bump_patch_resets_nothing(self) -> None:
        from jvis.commands.bump_cmd import _bump_semver

        assert _bump_semver("2.3.7", "patch") == "2.3.8"

    def test_bump_minor_resets_patch(self) -> None:
        from jvis.commands.bump_cmd import _bump_semver

        assert _bump_semver("2.3.7", "minor") == "2.4.0"

    def test_bump_major_resets_minor_and_patch(self) -> None:
        from jvis.commands.bump_cmd import _bump_semver

        assert _bump_semver("2.3.7", "major") == "3.0.0"

    def test_bump_invalid_version(self) -> None:
        import click

        from jvis.commands.bump_cmd import _bump_semver

        with pytest.raises(click.ClickException):
            _bump_semver("not-a-version", "patch")

    def test_bump_requires_part(self, runner: CliRunner) -> None:
        result = runner.invoke(cli, ["bump"])
        assert result.exit_code != 0

    def test_bump_rejects_invalid_part(self, runner: CliRunner) -> None:
        result = runner.invoke(cli, ["bump", "hotfix"])
        assert result.exit_code != 0

    def test_bump_syncs_version_yaml_components(self, tmp_path: Path) -> None:
        """_update_version_yaml syncs component versions to the new version."""
        from jvis.commands.bump_cmd import _update_version_yaml

        version_yaml = tmp_path / ".jvis" / "VERSION.yaml"
        version_yaml.parent.mkdir(parents=True)
        version_yaml.write_text(
            'version: 4.0.0\nrelease_date: "2026-01-01"\ncomponents:\n  cli: 4.0.0\n  agents: 3.9.0\n'
        )

        _update_version_yaml(tmp_path, "4.0.0", "4.1.0", dry_run=False)
        content = version_yaml.read_text()
        assert "version: 4.1.0" in content
        assert "cli: 4.1.0" in content
        assert "agents: 4.1.0" in content


# =============================================================================
# UPDATE COMMAND
# =============================================================================


class TestUpdateCommand:
    def test_update_no_jvis(self, runner: CliRunner, tmp_path) -> None:
        """Update should fail on a directory without JVIS."""
        result = runner.invoke(cli, ["update", str(tmp_path)])
        assert result.exit_code == 1
        assert "No JVIS installation" in result.output

    def test_update_already_current(self, runner: CliRunner, tmp_project) -> None:
        """Update should say 'up to date' when versions match."""
        from jvis.utils.config import read_version

        current = read_version()
        (tmp_project / ".jvis" / "version").write_text(f"{current}\n")
        result = runner.invoke(cli, ["update", str(tmp_project)])
        assert result.exit_code == 0
        assert "up to date" in result.output.lower()

    def test_update_dry_run(self, runner: CliRunner, tmp_project) -> None:
        """Dry run should show versions without changing files."""
        result = runner.invoke(cli, ["update", str(tmp_project), "--dry-run"])
        assert result.exit_code == 0
        assert "Dry run" in result.output or "no changes" in result.output.lower()
        # Config should not have provenance stamped
        config = (tmp_project / ".jvis" / "core-config.yaml").read_text()
        assert "jvis_installed_version" not in config


# =============================================================================
# VERSION TRACKING
# =============================================================================


class TestVersionTracking:
    def test_stamp_and_read_roundtrip(self, tmp_project) -> None:
        from jvis.version_tracking import read_provenance, stamp_version

        stamp_version(tmp_project, "4.1.0", "dev")
        prov = read_provenance(tmp_project)
        assert prov["jvis_installed_version"] == "4.1.0"
        assert prov["jvis_source"] == "dev"
        assert "jvis_installed_at" in prov

    def test_stamp_overwrites_existing(self, tmp_project) -> None:
        from jvis.version_tracking import read_provenance, stamp_version

        stamp_version(tmp_project, "4.0.0", "pip")
        stamp_version(tmp_project, "4.1.0", "dev")
        prov = read_provenance(tmp_project)
        assert prov["jvis_installed_version"] == "4.1.0"
        assert prov["jvis_source"] == "dev"

    def test_stamp_preserves_existing_config(self, tmp_project) -> None:
        from jvis.version_tracking import stamp_version

        stamp_version(tmp_project, "4.1.0", "dev")
        config = (tmp_project / ".jvis" / "core-config.yaml").read_text()
        assert "markdownExploder: true" in config
        assert "qaLocation: docs/qa" in config

    def test_read_provenance_missing_config(self, tmp_path) -> None:
        from jvis.version_tracking import read_provenance

        prov = read_provenance(tmp_path)
        assert prov == {}

    def test_stamp_without_existing_provenance(self, tmp_path) -> None:
        """stamp_version appends provenance to a config with no prior version info."""
        from jvis.version_tracking import read_provenance, stamp_version

        jvis_dir = tmp_path / ".jvis"
        jvis_dir.mkdir()
        (jvis_dir / "core-config.yaml").write_text("someKey: someValue\n")

        stamp_version(tmp_path, "4.2.0", "pip")
        prov = read_provenance(tmp_path)
        assert prov["jvis_installed_version"] == "4.2.0"
        # Original config content preserved
        content = (jvis_dir / "core-config.yaml").read_text()
        assert "someKey: someValue" in content

    def test_stamp_preserves_yaml_comments(self, tmp_path) -> None:
        """stamp_version uses regex replacement, not yaml.dump, so comments survive."""
        from jvis.version_tracking import stamp_version

        jvis_dir = tmp_path / ".jvis"
        jvis_dir.mkdir()
        (jvis_dir / "core-config.yaml").write_text("# Important comment\nqa:\n  qaLocation: docs/qa\n")

        stamp_version(tmp_path, "4.2.0", "dev")
        content = (jvis_dir / "core-config.yaml").read_text()
        assert "# Important comment" in content

    def test_read_provenance_no_jvis_dir(self, tmp_path) -> None:
        """read_provenance returns empty dict when .jvis dir doesn't exist."""
        from jvis.version_tracking import read_provenance

        prov = read_provenance(tmp_path / "nonexistent")
        assert prov == {}

    def test_stamp_skips_when_no_config(self, tmp_path) -> None:
        """stamp_version is a no-op when core-config.yaml doesn't exist."""
        from jvis.version_tracking import read_provenance, stamp_version

        (tmp_path / ".jvis").mkdir()
        # No core-config.yaml
        stamp_version(tmp_path, "4.2.0", "dev")  # should not raise
        assert read_provenance(tmp_path) == {}

    def test_detect_source_mode(self) -> None:
        from jvis.version_tracking import detect_source_mode

        mode = detect_source_mode()
        assert mode in ("dev", "pip")

"""Tests for jvis.version_tracking — stamp, read, and detect."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from jvis.version_tracking import detect_source_mode, read_provenance, stamp_version


@pytest.fixture
def project_dir(tmp_path: Path) -> Path:
    """Create a minimal project with core-config.yaml."""
    jvis_dir = tmp_path / ".jvis"
    jvis_dir.mkdir()
    config = jvis_dir / "core-config.yaml"
    config.write_text(yaml.dump({"project_name": "test", "qa": {"gate": "pass"}}))
    return tmp_path


class TestStampVersion:
    def test_stamp_creates_provenance(self, project_dir: Path):
        """stamp_version adds provenance keys to core-config.yaml."""
        stamp_version(project_dir, "1.0.0", "dev")
        provenance = read_provenance(project_dir)
        assert provenance["jvis_installed_version"] == "1.0.0"
        assert provenance["jvis_source"] == "dev"
        assert "jvis_installed_at" in provenance

    def test_stamp_updates_existing(self, project_dir: Path):
        """Stamping twice updates the values."""
        stamp_version(project_dir, "1.0.0", "dev")
        stamp_version(project_dir, "2.0.0", "pip")
        provenance = read_provenance(project_dir)
        assert provenance["jvis_installed_version"] == "2.0.0"
        assert provenance["jvis_source"] == "pip"

    def test_stamp_missing_config(self, tmp_path: Path, caplog: pytest.LogCaptureFixture):
        """Stamping a project without core-config.yaml warns and skips."""
        import logging

        with caplog.at_level(logging.WARNING):
            stamp_version(tmp_path, "1.0.0", "dev")
        assert "skipping" in caplog.text.lower()


class TestReadProvenance:
    def test_read_empty_project(self, tmp_path: Path):
        """Returns empty dict when no config exists."""
        assert read_provenance(tmp_path) == {}

    def test_read_existing(self, project_dir: Path):
        """Reads back stamped provenance."""
        stamp_version(project_dir, "3.0.0", "pip")
        result = read_provenance(project_dir)
        assert result["jvis_installed_version"] == "3.0.0"


class TestDetectSourceMode:
    def test_returns_dev_or_pip(self):
        """detect_source_mode returns either 'dev' or 'pip'."""
        mode = detect_source_mode()
        assert mode in ("dev", "pip")

    def test_dev_mode_in_repo(self):
        """In our repo (editable install), should return 'dev'."""
        mode = detect_source_mode()
        assert mode == "dev"

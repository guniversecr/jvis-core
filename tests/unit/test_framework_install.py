"""Tests for jvis.scaffold.framework — install_framework, _resolve_jvis_source, _copy_claude_md."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest

from jvis.scaffold.framework import (
    _JVIS_DIRS,
    _JVIS_FILES,
    _copy_claude_md,
    _copy_jvis_dir,
    _resolve_jvis_source,
    install_framework,
)


def _create_fake_jvis_source(base: Path) -> Path:
    """Create a minimal fake .jvis/ source directory for testing."""
    jvis = base / ".jvis"
    jvis.mkdir(parents=True, exist_ok=True)
    for dirname in _JVIS_DIRS:
        (jvis / dirname).mkdir(exist_ok=True)
        (jvis / dirname / "placeholder.txt").write_text("test")
    for filename in _JVIS_FILES:
        (jvis / filename).write_text("test")
    return base


class TestResolveJvisSource:
    """Tests for _resolve_jvis_source() — finding .jvis/ across modes."""

    def test_installed_mode_found(self, tmp_path: Path):
        data = tmp_path / "data"
        (data / ".jvis").mkdir(parents=True)
        result = _resolve_jvis_source(data)
        assert result == data / ".jvis"

    def test_dev_mode_found(self, tmp_path: Path):
        data = tmp_path / "data"
        data.mkdir()
        repo = tmp_path / "repo"
        (repo / ".jvis").mkdir(parents=True)

        with (
            patch("jvis.scaffold.framework.get_repo_root", return_value=repo),
            patch("jvis.scaffold.framework.get_jvis_home", return_value=tmp_path / "nope"),
        ):
            result = _resolve_jvis_source(data)
        assert result == repo / ".jvis"

    def test_jvis_home_fallback(self, tmp_path: Path):
        data = tmp_path / "data"
        data.mkdir()
        home = tmp_path / "home"
        (home / ".jvis").mkdir(parents=True)

        with (
            patch("jvis.scaffold.framework.get_repo_root", return_value=tmp_path / "nope"),
            patch("jvis.scaffold.framework.get_jvis_home", return_value=home),
        ):
            result = _resolve_jvis_source(data)
        assert result == home / ".jvis"

    def test_none_when_not_found(self, tmp_path: Path):
        nope = tmp_path / "nope"
        nope.mkdir()
        with (
            patch("jvis.scaffold.framework.get_repo_root", return_value=nope),
            patch("jvis.scaffold.framework.get_jvis_home", return_value=nope),
        ):
            result = _resolve_jvis_source(nope)
        assert result is None


class TestCopyJvisDir:
    """Tests for _copy_jvis_dir() — copying essential dirs and files."""

    def test_copies_all_existing_dirs(self, tmp_path: Path):
        src = _create_fake_jvis_source(tmp_path / "src")
        target = tmp_path / "target"
        target.mkdir()

        with (
            patch("jvis.scaffold.framework.get_repo_root", return_value=tmp_path / "nope"),
            patch("jvis.scaffold.framework.get_jvis_home", return_value=tmp_path / "nope"),
        ):
            result = _copy_jvis_dir(src, target)

        assert result is True
        for dirname in _JVIS_DIRS:
            assert (target / ".jvis" / dirname).is_dir()

    def test_copies_files(self, tmp_path: Path):
        src = _create_fake_jvis_source(tmp_path / "src")
        target = tmp_path / "target"
        target.mkdir()

        with (
            patch("jvis.scaffold.framework.get_repo_root", return_value=tmp_path / "nope"),
            patch("jvis.scaffold.framework.get_jvis_home", return_value=tmp_path / "nope"),
        ):
            _copy_jvis_dir(src, target)

        for filename in _JVIS_FILES:
            assert (target / ".jvis" / filename).is_file()

    def test_returns_false_when_source_missing(self, tmp_path: Path):
        nope = tmp_path / "nope"
        nope.mkdir()
        target = tmp_path / "target"
        target.mkdir()

        with (
            patch("jvis.scaffold.framework.get_repo_root", return_value=nope),
            patch("jvis.scaffold.framework.get_jvis_home", return_value=nope),
        ):
            result = _copy_jvis_dir(nope, target)
        assert result is False


class TestInstallFrameworkHappyPath:
    """Tests for install_framework() end-to-end with a fake source."""

    def test_installs_jvis_dir(self, tmp_path: Path):
        src = _create_fake_jvis_source(tmp_path / "src")
        # Also create .claude/commands for platform files
        commands = src / ".claude" / "commands"
        commands.mkdir(parents=True)
        (commands / "test.md").write_text("# test")

        target = tmp_path / "target"
        target.mkdir()

        with (
            patch("jvis.scaffold.framework.get_data_dir", return_value=src),
            patch("jvis.scaffold.framework.get_repo_root", return_value=src),
            patch("jvis.scaffold.framework.get_jvis_home", return_value=tmp_path / "nope"),
        ):
            install_framework(target)

        assert (target / ".jvis").is_dir()
        assert (target / ".jvis" / "agents").is_dir()

    def test_raises_when_source_not_found(self, tmp_path: Path):
        nope = tmp_path / "nope"
        nope.mkdir()

        with (
            patch("jvis.scaffold.framework.get_data_dir", return_value=nope),
            patch("jvis.scaffold.framework.get_repo_root", return_value=nope),
            patch("jvis.scaffold.framework.get_jvis_home", return_value=nope),
            pytest.raises(RuntimeError, match="JVIS framework source"),
        ):
            install_framework(tmp_path / "target")


class TestCopyClaudeMd:
    """Tests for _copy_claude_md() — CLAUDE.md generation logic."""

    def test_does_not_overwrite_existing(self, tmp_path: Path):
        target = tmp_path / "project"
        target.mkdir()
        claude_md = target / "CLAUDE.md"
        claude_md.write_text("# My existing CLAUDE.md")

        data = tmp_path / "data"
        data.mkdir()

        with patch("jvis.scaffold.framework.get_repo_root", return_value=tmp_path / "nope"):
            _copy_claude_md(data, target)

        assert claude_md.read_text() == "# My existing CLAUDE.md"

    def test_generates_minimal_when_no_template(self, tmp_path: Path):
        target = tmp_path / "project"
        target.mkdir()

        data = tmp_path / "data"
        data.mkdir()

        with patch("jvis.scaffold.framework.get_repo_root", return_value=tmp_path / "nope"):
            _copy_claude_md(data, target)

        claude_md = target / "CLAUDE.md"
        assert claude_md.is_file()
        content = claude_md.read_text()
        assert "JVIS" in content
        assert "AI-assisted development" in content

    def test_renders_template_when_available(self, tmp_path: Path):
        target = tmp_path / "project"
        target.mkdir()

        data = tmp_path / "data"
        templates = data / "templates"
        templates.mkdir(parents=True)
        (templates / "CLAUDE.md.j2").write_text("# {{ project_name }} CLAUDE.md")

        with patch("jvis.scaffold.framework.get_repo_root", return_value=tmp_path / "nope"):
            _copy_claude_md(data, target)

        content = (target / "CLAUDE.md").read_text()
        assert "project" in content

    def test_copies_from_repo_in_dev_mode(self, tmp_path: Path):
        target = tmp_path / "project"
        target.mkdir()

        data = tmp_path / "data"
        data.mkdir()

        repo = tmp_path / "repo"
        repo.mkdir()
        (repo / "CLAUDE.md").write_text("# Repo CLAUDE.md")

        with patch("jvis.scaffold.framework.get_repo_root", return_value=repo):
            _copy_claude_md(data, target)

        assert (target / "CLAUDE.md").read_text() == "# Repo CLAUDE.md"

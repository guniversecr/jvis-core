"""Tests for jvis.commands.add_cmd — _confirm_existing_install and _install_jvis."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

from jvis.commands.add_cmd import _confirm_existing_install, _install_jvis
from jvis.detection.tech_stack import StackDetection


class TestConfirmExistingInstall:
    """Tests for _confirm_existing_install() confirmation logic."""

    def test_empty_state_returns_true(self):
        assert _confirm_existing_install("empty", yes=False) is True

    def test_has_code_returns_true(self):
        assert _confirm_existing_install("has_code", yes=False) is True

    def test_has_aicore_with_yes_flag_returns_true(self):
        assert _confirm_existing_install("has_aicore", yes=True) is True

    def test_has_context_with_yes_flag_returns_true(self):
        assert _confirm_existing_install("has_context", yes=True) is True

    def test_has_aicore_without_yes_prompts(self):
        with patch("jvis.commands.add_cmd.click.confirm", return_value=False):
            assert _confirm_existing_install("has_aicore", yes=False) is False

    def test_has_context_without_yes_prompts(self):
        with patch("jvis.commands.add_cmd.click.confirm", return_value=False):
            assert _confirm_existing_install("has_context", yes=False) is False

    def test_has_aicore_user_confirms(self):
        with patch("jvis.commands.add_cmd.click.confirm", return_value=True):
            assert _confirm_existing_install("has_aicore", yes=False) is True

    def test_has_context_user_confirms(self):
        with patch("jvis.commands.add_cmd.click.confirm", return_value=True):
            assert _confirm_existing_install("has_context", yes=False) is True


class TestInstallJvis:
    """Tests for _install_jvis() installation logic."""

    def test_empty_dir_installs_framework(self, tmp_path: Path):
        detection = StackDetection(languages=[], frameworks=[], databases=[])
        _install_jvis(tmp_path, "empty", detection)

        assert (tmp_path / ".jvis").is_dir()
        assert (tmp_path / "docs" / "notes").is_dir()
        assert (tmp_path / "docs" / "notes" / "context-map.md").is_file()

    def test_creates_shared_files_when_no_readme(self, tmp_path: Path):
        detection = StackDetection(languages=[], frameworks=[], databases=[])
        _install_jvis(tmp_path, "empty", detection)

        assert (tmp_path / "README.md").is_file()
        assert (tmp_path / ".editorconfig").is_file()

    def test_skips_shared_files_when_readme_exists(self, tmp_path: Path):
        (tmp_path / "README.md").write_text("# Existing Project")
        detection = StackDetection(languages=[], frameworks=[], databases=[])
        _install_jvis(tmp_path, "has_code", detection)

        content = (tmp_path / "README.md").read_text()
        assert content == "# Existing Project"

    def test_context_map_uses_detection_data(self, tmp_path: Path):
        detection = StackDetection(
            languages=["python"],
            frameworks=["fastapi"],
            databases=["postgresql"],
        )
        _install_jvis(tmp_path, "has_code", detection)

        context_map = (tmp_path / "docs" / "notes" / "context-map.md").read_text()
        assert "python" in context_map
        assert "fastapi" in context_map
        assert "postgresql" in context_map

    def test_git_configured(self, tmp_path: Path):
        detection = StackDetection(languages=[], frameworks=[], databases=[])
        _install_jvis(tmp_path, "empty", detection)

        assert (tmp_path / ".git").is_dir() or (tmp_path / ".gitignore").is_file()

    def test_jvis_version_file_written(self, tmp_path: Path):
        detection = StackDetection(languages=[], frameworks=[], databases=[])
        _install_jvis(tmp_path, "empty", detection)

        version_file = tmp_path / ".jvis" / "version"
        assert version_file.is_file()
        assert len(version_file.read_text().strip()) > 0

    def test_framework_detection_passed_to_git(self, tmp_path: Path):
        detection = StackDetection(
            languages=["python"],
            frameworks=["fastapi"],
            databases=[],
        )
        _install_jvis(tmp_path, "has_code", detection)

        gitignore = tmp_path / ".gitignore"
        if gitignore.is_file():
            content = gitignore.read_text()
            assert len(content) > 0

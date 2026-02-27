"""Tests for jvis.utils.git — git detection, init, gitignore, setup."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest

from jvis.utils.git import (
    _GITIGNORE_SECTIONS,
    git_init,
    is_git_repo,
    setup_git,
    write_gitignore,
)

# =============================================================================
# is_git_repo
# =============================================================================


class TestIsGitRepo:
    def test_returns_true_for_git_repo(self, tmp_path: Path) -> None:
        (tmp_path / ".git").mkdir()
        with patch("jvis.utils.git.subprocess.run") as mock_run:
            mock_run.return_value.returncode = 0
            assert is_git_repo(tmp_path) is True

    def test_returns_false_for_non_repo(self, tmp_path: Path) -> None:
        with patch("jvis.utils.git.subprocess.run") as mock_run:
            mock_run.return_value.returncode = 128
            assert is_git_repo(tmp_path) is False

    def test_returns_false_when_git_not_installed(self, tmp_path: Path) -> None:
        with patch("jvis.utils.git.subprocess.run", side_effect=FileNotFoundError):
            assert is_git_repo(tmp_path) is False


# =============================================================================
# git_init
# =============================================================================


class TestGitInit:
    def test_success(self, tmp_path: Path) -> None:
        target = tmp_path / "new-project"
        with patch("jvis.utils.git.subprocess.run") as mock_run:
            mock_run.return_value.returncode = 0
            assert git_init(target) is True
        assert target.is_dir()
        mock_run.assert_called_once()

    def test_failure(self, tmp_path: Path) -> None:
        with patch("jvis.utils.git.subprocess.run") as mock_run:
            mock_run.return_value.returncode = 1
            assert git_init(tmp_path) is False

    def test_git_not_installed(self, tmp_path: Path) -> None:
        with patch("jvis.utils.git.subprocess.run", side_effect=FileNotFoundError):
            assert git_init(tmp_path) is False


# =============================================================================
# write_gitignore
# =============================================================================


class TestWriteGitignore:
    def test_default_sections(self, tmp_path: Path) -> None:
        write_gitignore(tmp_path)
        content = (tmp_path / ".gitignore").read_text()
        assert ".DS_Store" in content
        assert "__pycache__" not in content  # python section not included by default

    def test_python_section(self, tmp_path: Path) -> None:
        write_gitignore(tmp_path, ["general", "python"])
        content = (tmp_path / ".gitignore").read_text()
        assert ".DS_Store" in content
        assert "__pycache__" in content

    def test_unknown_section_ignored(self, tmp_path: Path) -> None:
        write_gitignore(tmp_path, ["general", "nonexistent"])
        content = (tmp_path / ".gitignore").read_text()
        assert ".DS_Store" in content

    def test_all_known_sections(self) -> None:
        for name in ("general", "jvis", "python", "node", "rust"):
            assert name in _GITIGNORE_SECTIONS


# =============================================================================
# setup_git
# =============================================================================


class TestSetupGit:
    def test_initializes_new_repo(self, tmp_path: Path) -> None:
        with (
            patch("jvis.utils.git.is_git_repo", return_value=False),
            patch("jvis.utils.git.git_init") as mock_init,
            patch("jvis.utils.git.write_gitignore") as mock_ignore,
        ):
            setup_git(tmp_path, "python-fastapi")
            mock_init.assert_called_once_with(tmp_path)
            mock_ignore.assert_called_once()
            sections = mock_ignore.call_args[0][1]
            assert "python" in sections

    def test_skips_init_if_already_repo(self, tmp_path: Path) -> None:
        with (
            patch("jvis.utils.git.is_git_repo", return_value=True),
            patch("jvis.utils.git.git_init") as mock_init,
            patch("jvis.utils.git.write_gitignore"),
        ):
            setup_git(tmp_path, "nodejs-express")
            mock_init.assert_not_called()

    def test_node_stack_includes_node_section(self, tmp_path: Path) -> None:
        with (
            patch("jvis.utils.git.is_git_repo", return_value=True),
            patch("jvis.utils.git.write_gitignore") as mock_ignore,
        ):
            setup_git(tmp_path, "nodejs-express")
            sections = mock_ignore.call_args[0][1]
            assert "node" in sections

    def test_rust_stack_includes_rust_section(self, tmp_path: Path) -> None:
        with (
            patch("jvis.utils.git.is_git_repo", return_value=True),
            patch("jvis.utils.git.write_gitignore") as mock_ignore,
        ):
            setup_git(tmp_path, "rust-axum")
            sections = mock_ignore.call_args[0][1]
            assert "rust" in sections

    @pytest.mark.parametrize("stack_id", ["angular", "custom", "php-laravel"])
    def test_non_matching_stack_gets_only_general_and_jvis(self, tmp_path: Path, stack_id: str) -> None:
        with (
            patch("jvis.utils.git.is_git_repo", return_value=True),
            patch("jvis.utils.git.write_gitignore") as mock_ignore,
        ):
            setup_git(tmp_path, stack_id)
            sections = mock_ignore.call_args[0][1]
            assert sections == ["general", "jvis"]

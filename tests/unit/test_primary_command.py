"""Tests for jvis.commands.primary — _collect_config_scripted and _scaffold_project."""

from __future__ import annotations

from pathlib import Path

import click
import pytest

from jvis.commands.primary import ProjectConfig, _collect_config_scripted, _scaffold_project
from jvis.stacks.registry import get_stack


class TestCollectConfigScripted:
    """Unit tests for _collect_config_scripted() validation logic."""

    def test_valid_name_returns_project_config(self, tmp_path: Path):
        dest = tmp_path / "my-api"
        config = _collect_config_scripted("my-api", "python-fastapi", str(dest), "postgresql")

        assert isinstance(config, ProjectConfig)
        assert config.project_name == "my-api"
        assert config.project_dir == dest
        assert config.project_type == "single"
        assert config.database == "postgresql"
        assert config.stacks["stack"] is not None
        assert config.stacks["stack"].id == "python-fastapi"

    def test_name_sanitized(self, tmp_path: Path):
        dest = tmp_path / "proj"
        config = _collect_config_scripted("My Project", "custom", str(dest), None)
        assert config.project_name == "my-project"

    def test_invalid_name_raises(self, tmp_path: Path):
        with pytest.raises(click.ClickException, match="must start with a letter"):
            _collect_config_scripted("1bad", "custom", str(tmp_path / "x"), None)

    def test_empty_name_raises(self, tmp_path: Path):
        with pytest.raises(click.ClickException, match="cannot be empty"):
            _collect_config_scripted("---", "custom", str(tmp_path / "x"), None)

    def test_unknown_stack_raises_with_available_list(self, tmp_path: Path):
        with pytest.raises(click.ClickException, match="Unknown stack 'nonexistent'") as exc_info:
            _collect_config_scripted("my-proj", "nonexistent", str(tmp_path / "x"), None)
        assert "Available:" in str(exc_info.value.message)
        assert "python-fastapi" in str(exc_info.value.message)

    def test_invalid_db_raises(self, tmp_path: Path):
        with pytest.raises(click.ClickException, match="Unknown database 'mongodb'"):
            _collect_config_scripted("my-proj", "python-fastapi", str(tmp_path / "x"), "mongodb")

    def test_stack_without_db_leaves_database_empty(self, tmp_path: Path):
        config = _collect_config_scripted("my-app", "react-vite", str(tmp_path / "x"), None)
        assert config.database == ""

    def test_stack_with_db_defaults_to_postgresql(self, tmp_path: Path):
        config = _collect_config_scripted("my-api", "python-fastapi", str(tmp_path / "x"), None)
        assert config.database == "postgresql"

    def test_stack_with_explicit_mysql(self, tmp_path: Path):
        config = _collect_config_scripted("my-api", "python-fastapi", str(tmp_path / "x"), "mysql")
        assert config.database == "mysql"

    def test_stacks_dict_structure(self, tmp_path: Path):
        config = _collect_config_scripted("my-api", "python-fastapi", str(tmp_path / "x"), None)
        assert "stack" in config.stacks
        assert "backend" in config.stacks
        assert "frontend" in config.stacks
        assert "mobile" in config.stacks
        assert config.stacks["backend"] is None
        assert config.stacks["frontend"] is None
        assert config.stacks["mobile"] is None

    def test_path_expanded_and_resolved(self, tmp_path: Path):
        config = _collect_config_scripted("my-api", "custom", str(tmp_path / "x"), None)
        assert config.project_dir.is_absolute()

    def test_entity_default_is_item(self, tmp_path: Path):
        config = _collect_config_scripted("my-app", "custom", str(tmp_path / "x"), None)
        assert config.entity_name == "item"

    def test_entity_flag_stored_in_config(self, tmp_path: Path):
        config = _collect_config_scripted("my-app", "custom", str(tmp_path / "x"), None, "product")
        assert config.entity_name == "product"

    def test_entity_invalid_raises(self, tmp_path: Path):
        with pytest.raises(click.ClickException, match="lowercase letters only"):
            _collect_config_scripted("my-app", "custom", str(tmp_path / "x"), None, "My-Item")

    def test_entity_too_short_raises(self, tmp_path: Path):
        with pytest.raises(click.ClickException, match="at least 2 characters"):
            _collect_config_scripted("my-app", "custom", str(tmp_path / "x"), None, "x")


class TestScaffoldProject:
    """Integration tests for _scaffold_project() with a real tmp_path."""

    def _make_config(self, tmp_path: Path, stack_id: str = "python-fastapi", db: str = "postgresql") -> ProjectConfig:
        stack = get_stack(stack_id)
        stacks = {"stack": stack, "backend": None, "frontend": None, "mobile": None}
        return ProjectConfig(
            project_name="test-proj",
            project_description="Test project",
            project_dir=tmp_path / "test-proj",
            project_type="single",
            stacks=stacks,
            database=db,
        )

    def test_single_stack_creates_full_structure(self, tmp_path: Path):
        config = self._make_config(tmp_path)
        _scaffold_project(config)
        project = config.project_dir

        assert project.is_dir()
        assert (project / ".jvis").is_dir()
        assert (project / "docs" / "notes").is_dir()
        assert (project / "docs" / "notes" / "context-map.md").is_file()

    def test_shared_files_created(self, tmp_path: Path):
        config = self._make_config(tmp_path)
        _scaffold_project(config)
        project = config.project_dir

        assert (project / ".editorconfig").is_file()
        assert (project / "README.md").is_file()
        assert (project / "CHANGELOG.md").is_file()

    def test_git_initialized(self, tmp_path: Path):
        config = self._make_config(tmp_path)
        _scaffold_project(config)
        project = config.project_dir

        assert (project / ".git").is_dir() or (project / ".gitignore").is_file()

    def test_jvis_version_file_written(self, tmp_path: Path):
        config = self._make_config(tmp_path)
        _scaffold_project(config)
        project = config.project_dir

        version_file = project / ".jvis" / "version"
        assert version_file.is_file()
        assert len(version_file.read_text().strip()) > 0

    def test_stack_files_generated(self, tmp_path: Path):
        config = self._make_config(tmp_path, "python-fastapi", "postgresql")
        _scaffold_project(config)
        project = config.project_dir

        assert (project / "pyproject.toml").is_file()
        assert (project / "src" / "main.py").is_file()

    def test_frontend_stack_no_db(self, tmp_path: Path):
        config = self._make_config(tmp_path, "react-vite", "")
        _scaffold_project(config)
        project = config.project_dir

        assert (project / "package.json").is_file()
        assert (project / ".jvis").is_dir()

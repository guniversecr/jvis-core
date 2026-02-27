"""Tests for jvis.detection modules."""

from __future__ import annotations

from jvis.detection.project_state import detect_project_state
from jvis.detection.tech_stack import detect_project_type, detect_tech_stack


class TestDetectProjectState:
    def test_empty_dir(self, tmp_path):
        assert detect_project_state(tmp_path) == "empty"

    def test_nonexistent_dir(self, tmp_path):
        assert detect_project_state(tmp_path / "nope") == "empty"

    def test_has_code_pyproject(self, tmp_path):
        (tmp_path / "pyproject.toml").write_text("[project]\nname = 'test'\n")
        assert detect_project_state(tmp_path) == "has_code"

    def test_has_code_package_json(self, tmp_path):
        (tmp_path / "package.json").write_text('{"name": "test"}')
        assert detect_project_state(tmp_path) == "has_code"

    def test_has_code_source_files(self, tmp_path):
        (tmp_path / "main.py").write_text("print('hello')")
        assert detect_project_state(tmp_path) == "has_code"

    def test_has_aicore(self, tmp_path):
        (tmp_path / ".jvis").mkdir()
        assert detect_project_state(tmp_path) == "has_aicore"

    def test_has_context(self, tmp_path):
        (tmp_path / ".jvis").mkdir()
        notes = tmp_path / "docs" / "notes"
        notes.mkdir(parents=True)
        log = notes / "project-log.md"
        log.write_text("# Log\n---\nEntry 1\n---\nEntry 2\n---\n")
        assert detect_project_state(tmp_path) == "has_context"

    def test_has_ideation(self, tmp_path):
        (tmp_path / "market-research.md").write_text("# Research\n")
        assert detect_project_state(tmp_path) == "has_ideation"

    def test_priority_aicore_over_code(self, tmp_path):
        (tmp_path / ".jvis").mkdir()
        (tmp_path / "pyproject.toml").write_text("[project]\n")
        assert detect_project_state(tmp_path) == "has_aicore"


class TestDetectTechStack:
    def test_empty_dir(self, tmp_path):
        result = detect_tech_stack(tmp_path)
        assert result.summary == "unknown"

    def test_python_project(self, tmp_path):
        (tmp_path / "pyproject.toml").write_text("[project]\ndependencies=['fastapi']\n")
        result = detect_tech_stack(tmp_path)
        assert "python" in result.languages
        assert "fastapi" in result.frameworks
        assert "api" in result.recommended_agents

    def test_node_project(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies": {"express": "^4.0", "prisma": "^5.0"}}')
        result = detect_tech_stack(tmp_path)
        assert "node" in result.languages
        assert "express" in result.frameworks
        assert "prisma" in result.recommended_agents

    def test_rust_project(self, tmp_path):
        (tmp_path / "Cargo.toml").write_text('[dependencies]\naxum = "0.7"\n')
        result = detect_tech_stack(tmp_path)
        assert "rust" in result.languages
        assert "axum" in result.frameworks
        assert "rust" in result.recommended_agents

    def test_docker_detection(self, tmp_path):
        (tmp_path / "Dockerfile").write_text("FROM python:3.12\n")
        result = detect_tech_stack(tmp_path)
        assert "docker" in result.frameworks

    def test_core_agents_always_included(self, tmp_path):
        result = detect_tech_stack(tmp_path)
        for agent in ("pm", "architect", "sm", "dev", "qa"):
            assert agent in result.recommended_agents

    def test_monorepo_subdir_python(self, tmp_path):
        """Detect Python in a subdirectory (monorepo pattern)."""
        backend = tmp_path / "backend"
        backend.mkdir()
        (backend / "pyproject.toml").write_text("[project]\ndependencies=['fastapi']\n")
        result = detect_tech_stack(tmp_path)
        assert "python" in result.languages
        assert "fastapi" in result.frameworks

    def test_monorepo_subdir_node(self, tmp_path):
        """Detect Node.js in a subdirectory (monorepo pattern)."""
        frontend = tmp_path / "frontend"
        frontend.mkdir()
        (frontend / "package.json").write_text('{"dependencies": {"react": "^18"}}')
        result = detect_tech_stack(tmp_path)
        assert "node" in result.languages
        assert "react" in result.frameworks

    def test_monorepo_multiple_subdirs(self, tmp_path):
        """Detect multiple stacks across subdirectories."""
        backend = tmp_path / "backend"
        backend.mkdir()
        (backend / "pyproject.toml").write_text("[project]\n")
        frontend = tmp_path / "frontend"
        frontend.mkdir()
        (frontend / "package.json").write_text('{"dependencies": {"react": "^18"}}')
        result = detect_tech_stack(tmp_path)
        assert "python" in result.languages
        assert "node" in result.languages
        assert "react" in result.frameworks

    def test_monorepo_skips_dotdirs(self, tmp_path):
        """Dotfiles like .venv/ should not be scanned."""
        venv = tmp_path / ".venv"
        venv.mkdir()
        (venv / "pyproject.toml").write_text("[project]\n")
        result = detect_tech_stack(tmp_path)
        assert "python" not in result.languages

    def test_monorepo_no_deep_recursion(self, tmp_path):
        """Only scan 1 level deep, not deeper subdirectories."""
        deep = tmp_path / "a" / "b"
        deep.mkdir(parents=True)
        (deep / "Cargo.toml").write_text('[dependencies]\naxum = "0.7"\n')
        result = detect_tech_stack(tmp_path)
        assert "rust" not in result.languages


class TestDetectProjectType:
    def test_single(self, tmp_path):
        assert detect_project_type(tmp_path) == "single"

    def test_fullstack(self, tmp_path):
        (tmp_path / "server").mkdir()
        (tmp_path / "client").mkdir()
        assert detect_project_type(tmp_path) == "fullstack"

    def test_fullstack_mobile(self, tmp_path):
        (tmp_path / "server").mkdir()
        (tmp_path / "client").mkdir()
        (tmp_path / "mobile").mkdir()
        assert detect_project_type(tmp_path) == "fullstack-mobile"

    def test_saas_platform(self, tmp_path):
        (tmp_path / "server").mkdir()
        (tmp_path / "client").mkdir()
        (tmp_path / "infra").mkdir()
        assert detect_project_type(tmp_path) == "saas-platform"

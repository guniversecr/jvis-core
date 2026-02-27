"""Integration test for `jvis new` — end-to-end in a temp directory."""

from __future__ import annotations

from pathlib import Path

from click.testing import CliRunner

from jvis.cli import cli


class TestNewCommandIntegration:
    """Test `jvis new` with simulated interactive input.

    The interactive flow for a "single" project type uses a hierarchical menu:
      1. Project name
      2. Description
      3. Location (1=cwd, 2=~/Projects, 3=custom path)
      4. Project type (1=single, 2=fullstack, 3=fullstack-mobile, 4=saas)
      5. Category (1=backend, 2=frontend, 3=fullstack, 4=custom)
      6. Language (if multiple in category)
      7. Framework (if multiple in language)
      8. Database (if stack requires it)
      9. Confirmation (y/n)

    For "fullstack" project type, backend and frontend use flat selection.
    """

    def test_new_single_python_fastapi(self, tmp_path: Path):
        """Full flow: single-stack, python-fastapi, postgresql."""
        project_dir = tmp_path / "test-api"

        runner = CliRunner()
        # Hierarchical: category=1(backend), language=3(python), framework=2(fastapi)
        # Backend languages: 1=typescript, 2=php, 3=python, 4=rust
        # Python frameworks: 1=django, 2=fastapi, 3=flask
        # Database: 1=postgresql
        result = runner.invoke(
            cli,
            ["new"],
            input=f"test-api\nTest API\n3\n{project_dir}\n1\n1\n3\n2\n1\ny\n",
        )

        # Should succeed
        assert result.exit_code == 0, f"Failed with output:\n{result.output}"
        assert "Project Created" in result.output or "test-api" in result.output

        # Project directory should exist with JVIS framework + docs
        assert project_dir.is_dir()
        assert (project_dir / ".jvis").is_dir()
        assert (project_dir / "docs" / "notes").is_dir()
        assert (project_dir / "docs" / "notes" / "context-map.md").is_file()
        assert (project_dir / "CLAUDE.md").is_file()
        assert (project_dir / ".editorconfig").is_file()

    def test_new_single_custom(self, tmp_path: Path):
        """Single-stack with custom (minimal) stack."""
        project_dir = tmp_path / "minimal-proj"

        runner = CliRunner()
        # Hierarchical: type=1(single), category=1(backend), language=1(python), framework=1(custom)
        # No database prompt (custom doesn't require one)
        result = runner.invoke(
            cli,
            ["new"],
            input=f"minimal-proj\n\n3\n{project_dir}\n1\n1\n1\n1\ny\n",
        )

        assert result.exit_code == 0, f"Failed with output:\n{result.output}"
        assert project_dir.is_dir()

    def test_new_fullstack(self, tmp_path: Path):
        """Fullstack project with backend + frontend."""
        project_dir = tmp_path / "full-proj"

        runner = CliRunner()
        # Type=2 (fullstack) → flat backend selection, flat frontend selection
        # Backend flat: 1=nodejs-express, ... 7=python-fastapi ...
        # Frontend flat: 1=angular, ... 3=react-vite ...
        # Database: 1=postgresql
        result = runner.invoke(
            cli,
            ["new"],
            input=f"full-proj\nFull project\n3\n{project_dir}\n2\n1\n3\n1\ny\n",
        )

        assert result.exit_code == 0, f"Failed with output:\n{result.output}"
        assert project_dir.is_dir()
        # Monorepo should have server/ and client/
        assert (project_dir / "server").is_dir()
        assert (project_dir / "client").is_dir()
        assert (project_dir / "docker-compose.yaml").is_file()
        assert (project_dir / "Makefile").is_file()

    def test_new_with_custom_entity(self, tmp_path: Path):
        """Single-stack with custom entity name replaces 'item' references."""
        project_dir = tmp_path / "shop-app"

        runner = CliRunner()
        result = runner.invoke(
            cli,
            ["new", "--name", "shop-app", "--stack", "custom", "--path", str(project_dir), "--entity", "product", "-y"],
        )

        assert result.exit_code == 0, f"Failed with output:\n{result.output}"
        assert project_dir.is_dir()
        assert "Applying entity name" in result.output

    def test_new_cancelled(self, tmp_path: Path):
        """User cancels at confirmation step."""
        runner = CliRunner()
        # Hierarchical: category=1(backend), language=1(python), stack=1(custom), confirm=n
        result = runner.invoke(
            cli,
            ["new"],
            input=f"cancel-proj\n\n3\n{tmp_path / 'cancel-proj'}\n1\n1\n1\n1\nn\n",
        )

        assert result.exit_code == 0
        assert not (tmp_path / "cancel-proj").is_dir()


class TestAddCommandIntegration:
    """Test `jvis add` with real directories."""

    def test_add_to_empty_dir(self, tmp_path: Path):
        """Add JVIS to an empty directory."""
        target = tmp_path / "existing"
        target.mkdir()

        runner = CliRunner()
        result = runner.invoke(
            cli,
            ["add", str(target)],
            input="y\n",
        )

        assert result.exit_code == 0, f"Failed with output:\n{result.output}"
        assert "JVIS Added Successfully" in result.output or "JVIS installed" in result.output

        # Should have full JVIS structure
        assert (target / ".jvis").is_dir()
        assert (target / "docs" / "notes").is_dir()
        assert (target / "docs" / "notes" / "context-map.md").is_file()
        assert (target / "CLAUDE.md").is_file()

    def test_add_to_python_project(self, tmp_path: Path):
        """Add JVIS to a directory with a pyproject.toml."""
        target = tmp_path / "py-project"
        target.mkdir()
        (target / "pyproject.toml").write_text("[project]\nname = 'test'\n")
        (target / "src").mkdir()

        runner = CliRunner()
        result = runner.invoke(
            cli,
            ["add", str(target)],
            input="y\n",
        )

        assert result.exit_code == 0, f"Failed with output:\n{result.output}"
        # Should detect as brownfield with python
        assert "has_code" in result.output or "Brownfield" in result.output
        assert "python" in result.output.lower()

    def test_add_nonexistent_dir(self, tmp_path: Path):
        """Add to a non-existent directory should fail."""
        runner = CliRunner()
        result = runner.invoke(cli, ["add", str(tmp_path / "nope")])

        assert result.exit_code == 1
        assert "does not exist" in result.output

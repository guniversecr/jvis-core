"""E2E Wheel Verification Tests.

Builds the wheel, installs it in a clean venv, and verifies
that `jvis new` and `jvis add` produce the correct project structure.

Run with: JVIS_E2E=1 pytest tests/integration/test_wheel_install.py -v

These tests are slow (~30s) because they build a wheel and create a venv.
They are skipped in CI unless JVIS_E2E=1 is set.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).parent.parent.parent

# Skip unless JVIS_E2E=1 is set (these are slow, build a wheel + venv)
pytestmark = pytest.mark.skipif(
    os.environ.get("JVIS_E2E") != "1",
    reason="Slow E2E test — set JVIS_E2E=1 to run",
)


@pytest.fixture(scope="module")
def wheel_path(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """Build the wheel once for all tests in this module."""
    dist_dir = tmp_path_factory.mktemp("dist")
    result = subprocess.run(
        [sys.executable, "-m", "build", "--wheel", "--outdir", str(dist_dir)],
        cwd=str(PROJECT_ROOT),
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert result.returncode == 0, f"Wheel build failed:\n{result.stderr}"
    wheels = list(dist_dir.glob("jvis-*.whl"))
    assert len(wheels) == 1, f"Expected 1 wheel, found {len(wheels)}: {wheels}"
    return wheels[0]


@pytest.fixture(scope="module")
def venv_dir(tmp_path_factory: pytest.TempPathFactory, wheel_path: Path) -> Path:
    """Create a clean venv and install the wheel."""
    venv = tmp_path_factory.mktemp("venv")

    # Create venv
    subprocess.run(
        [sys.executable, "-m", "venv", str(venv)],
        check=True,
        timeout=30,
    )

    pip = venv / "bin" / "pip"
    # Install wheel with dependencies
    subprocess.run(
        [str(pip), "install", str(wheel_path)],
        check=True,
        capture_output=True,
        timeout=60,
    )
    return venv


@pytest.fixture(scope="module")
def venv_python(venv_dir: Path) -> Path:
    """Return path to the venv's python."""
    return venv_dir / "bin" / "python"


@pytest.fixture(scope="module")
def venv_jvis(venv_dir: Path) -> Path:
    """Return path to the venv's jvis console script."""
    return venv_dir / "bin" / "jvis"


class TestWheelContents:
    """Verify the wheel contains all expected files."""

    def test_jvis_cli_exists(self, venv_jvis: Path) -> None:
        """The `jvis` console script is installed."""
        assert venv_jvis.is_file()

    def test_version_command(self, venv_python: Path) -> None:
        """jvis --version works from the installed wheel."""
        result = subprocess.run(
            [str(venv_python), "-m", "jvis", "--version"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        assert result.returncode == 0
        assert "JVIS Manager" in result.stdout and "4." in result.stdout

    def test_data_dir_has_jvis(self, venv_python: Path) -> None:
        """get_data_dir() finds .jvis/ in installed package."""
        code = "from jvis.utils.paths import get_data_dir; d = get_data_dir(); print(d); print((d / '.jvis').is_dir())"
        result = subprocess.run(
            [str(venv_python), "-c", code],
            capture_output=True,
            text=True,
            timeout=10,
        )
        assert result.returncode == 0, f"Failed:\n{result.stderr}"
        lines = result.stdout.strip().split("\n")
        assert lines[-1] == "True", f"data/.jvis/ not found. Output: {result.stdout}"

    def test_data_dir_has_agents(self, venv_python: Path) -> None:
        """Bundled .jvis/ contains agents directory."""
        code = (
            "from jvis.utils.paths import get_data_dir; "
            "d = get_data_dir() / '.jvis' / 'agents'; "
            "print(d.is_dir()); "
            "print(len(list(d.iterdir())) if d.is_dir() else 0)"
        )
        result = subprocess.run(
            [str(venv_python), "-c", code],
            capture_output=True,
            text=True,
            timeout=10,
        )
        assert result.returncode == 0
        lines = result.stdout.strip().split("\n")
        assert lines[0] == "True", "agents/ not bundled in wheel"
        assert int(lines[1]) >= 4, f"Expected 4+ agent packs, got {lines[1]}"

    def test_data_dir_has_commands(self, venv_python: Path) -> None:
        """Bundled data/ contains commands (slash commands)."""
        code = (
            "from jvis.utils.paths import get_data_dir; "
            "d = get_data_dir() / 'commands'; "
            "print(d.is_dir()); "
            "mds = list(d.glob('*.md')) if d.is_dir() else []; "
            "print(len(mds))"
        )
        result = subprocess.run(
            [str(venv_python), "-c", code],
            capture_output=True,
            text=True,
            timeout=10,
        )
        assert result.returncode == 0
        lines = result.stdout.strip().split("\n")
        assert lines[0] == "True", "commands/ not bundled in wheel"
        assert int(lines[1]) >= 8, f"Expected 8+ command files, got {lines[1]}"

    def test_data_dir_has_skills(self, venv_python: Path) -> None:
        """Bundled data/ contains skills directory."""
        code = "from jvis.utils.paths import get_data_dir; d = get_data_dir() / 'skills'; print(d.is_dir())"
        result = subprocess.run(
            [str(venv_python), "-c", code],
            capture_output=True,
            text=True,
            timeout=10,
        )
        assert result.returncode == 0
        assert "True" in result.stdout, "skills/ not bundled in wheel"

    def test_data_dir_has_hooks(self, venv_python: Path) -> None:
        """Bundled data/ contains hooks directory."""
        code = "from jvis.utils.paths import get_data_dir; d = get_data_dir() / 'hooks'; print(d.is_dir())"
        result = subprocess.run(
            [str(venv_python), "-c", code],
            capture_output=True,
            text=True,
            timeout=10,
        )
        assert result.returncode == 0
        assert "True" in result.stdout, "hooks/ not bundled in wheel"


class TestJvisAddFromWheel:
    """Test that `jvis add` works from the installed wheel."""

    def test_add_creates_jvis_dir(self, venv_python: Path, tmp_path: Path) -> None:
        """jvis add <dir> creates .jvis/ with expected subdirs."""
        target = tmp_path / "test-project"
        target.mkdir()

        result = subprocess.run(
            [str(venv_python), "-m", "jvis", "add", str(target)],
            input="y\n",
            capture_output=True,
            text=True,
            timeout=30,
        )
        assert result.returncode == 0, f"jvis add failed:\n{result.output}\n{result.stderr}"

        # .jvis/ should exist with key subdirs
        jvis_dir = target / ".jvis"
        assert jvis_dir.is_dir(), ".jvis/ not created by jvis add"

        for subdir in ("agents", "tasks", "templates"):
            assert (jvis_dir / subdir).is_dir(), f".jvis/{subdir}/ missing after jvis add"

    def test_add_creates_claude_commands(self, venv_python: Path, tmp_path: Path) -> None:
        """jvis add creates .claude/commands/ with slash command files."""
        target = tmp_path / "cmd-project"
        target.mkdir()

        subprocess.run(
            [str(venv_python), "-m", "jvis", "add", str(target)],
            input="y\n",
            capture_output=True,
            text=True,
            timeout=30,
        )

        commands_dir = target / ".claude" / "commands"
        assert commands_dir.is_dir(), ".claude/commands/ not created"
        md_files = list(commands_dir.glob("*.md"))
        assert len(md_files) >= 8, f"Expected 8+ slash commands, found {len(md_files)}"

    def test_add_creates_claude_extras(self, venv_python: Path, tmp_path: Path) -> None:
        """jvis add creates .claude/skills/ and .claude/hooks/."""
        target = tmp_path / "extras-project"
        target.mkdir()

        subprocess.run(
            [str(venv_python), "-m", "jvis", "add", str(target)],
            input="y\n",
            capture_output=True,
            text=True,
            timeout=30,
        )

        assert (target / ".claude" / "skills").is_dir(), ".claude/skills/ not created"
        assert (target / ".claude" / "hooks").is_dir(), ".claude/hooks/ not created"

    def test_add_creates_docs_structure(self, venv_python: Path, tmp_path: Path) -> None:
        """jvis add creates docs/ structure."""
        target = tmp_path / "docs-project"
        target.mkdir()

        subprocess.run(
            [str(venv_python), "-m", "jvis", "add", str(target)],
            input="y\n",
            capture_output=True,
            text=True,
            timeout=30,
        )

        assert (target / "docs" / "notes").is_dir(), "docs/notes/ not created"

    def test_add_creates_claude_md(self, venv_python: Path, tmp_path: Path) -> None:
        """jvis add creates CLAUDE.md."""
        target = tmp_path / "claude-md-project"
        target.mkdir()

        subprocess.run(
            [str(venv_python), "-m", "jvis", "add", str(target)],
            input="y\n",
            capture_output=True,
            text=True,
            timeout=30,
        )

        claude_md = target / "CLAUDE.md"
        assert claude_md.is_file(), "CLAUDE.md not created"
        content = claude_md.read_text()
        assert "JVIS" in content


class TestJvisNewFromWheel:
    """Test that `jvis new` works from the installed wheel (non-interactive flags)."""

    def test_new_custom_stack(self, venv_python: Path, tmp_path: Path) -> None:
        """jvis new --stack custom creates a minimal project."""
        project_dir = tmp_path / "new-minimal"

        result = subprocess.run(
            [
                str(venv_python),
                "-m",
                "jvis",
                "new",
                "--name",
                "new-minimal",
                "--stack",
                "custom",
                "--path",
                str(project_dir),
                "-y",
            ],
            capture_output=True,
            text=True,
            timeout=60,
        )
        assert result.returncode == 0, f"jvis new failed:\n{result.stdout}\n{result.stderr}"

        # Project structure
        assert project_dir.is_dir(), "Project directory not created"
        assert (project_dir / ".jvis").is_dir(), ".jvis/ missing from new project"
        assert (project_dir / "docs" / "notes").is_dir(), "docs/notes/ missing"
        assert (project_dir / "CLAUDE.md").is_file(), "CLAUDE.md missing"

    def test_new_python_fastapi(self, venv_python: Path, tmp_path: Path) -> None:
        """jvis new --stack python-fastapi creates a FastAPI project with full structure."""
        project_dir = tmp_path / "new-api"

        result = subprocess.run(
            [
                str(venv_python),
                "-m",
                "jvis",
                "new",
                "--name",
                "new-api",
                "--stack",
                "python-fastapi",
                "--path",
                str(project_dir),
                "--database",
                "postgresql",
                "-y",
            ],
            capture_output=True,
            text=True,
            timeout=60,
        )
        assert result.returncode == 0, f"jvis new failed:\n{result.stdout}\n{result.stderr}"

        # JVIS framework files
        assert (project_dir / ".jvis").is_dir(), ".jvis/ missing"
        assert (project_dir / ".jvis" / "agents").is_dir(), ".jvis/agents/ missing"
        assert (project_dir / ".claude" / "commands").is_dir(), ".claude/commands/ missing"
        assert (project_dir / "CLAUDE.md").is_file(), "CLAUDE.md missing"
        assert (project_dir / "docs" / "notes").is_dir(), "docs/notes/ missing"

        # Stack-generated files (FastAPI scaffold)
        assert (project_dir / "pyproject.toml").is_file() or (project_dir / "requirements.txt").is_file(), (
            "No Python project file found"
        )

    def test_new_react_vite(self, venv_python: Path, tmp_path: Path) -> None:
        """jvis new --stack react-vite creates a React project."""
        project_dir = tmp_path / "new-ui"

        result = subprocess.run(
            [
                str(venv_python),
                "-m",
                "jvis",
                "new",
                "--name",
                "new-ui",
                "--stack",
                "react-vite",
                "--path",
                str(project_dir),
                "-y",
            ],
            capture_output=True,
            text=True,
            timeout=60,
        )
        assert result.returncode == 0, f"jvis new failed:\n{result.stdout}\n{result.stderr}"

        # JVIS framework
        assert (project_dir / ".jvis").is_dir(), ".jvis/ missing"
        assert (project_dir / "CLAUDE.md").is_file(), "CLAUDE.md missing"

        # Stack-generated files (React scaffold)
        assert (project_dir / "package.json").is_file() or (project_dir / "tsconfig.json").is_file(), (
            "No frontend project file found"
        )

    def test_new_invalid_stack_fails(self, venv_python: Path, tmp_path: Path) -> None:
        """jvis new with an invalid stack name exits with error."""
        result = subprocess.run(
            [
                str(venv_python),
                "-m",
                "jvis",
                "new",
                "--name",
                "bad-proj",
                "--stack",
                "nonexistent-stack",
                "--path",
                str(tmp_path / "bad-proj"),
                "-y",
            ],
            capture_output=True,
            text=True,
            timeout=30,
        )
        assert result.returncode != 0, "Should fail for invalid stack"

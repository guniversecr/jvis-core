"""Package Install Tests.

Verifies that `pip install -e .` produces correct package structure.

Run with: pytest tests/integration/test_package_install.py -v
"""

from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent


def test_package_init_exists():
    """src/jvis/__init__.py exists with version."""
    init = PROJECT_ROOT / "src" / "jvis" / "__init__.py"
    assert init.exists()
    content = init.read_text()
    assert "__version__" in content


def test_cli_module_exists():
    """src/jvis/cli.py exists with main entry point."""
    cli = PROJECT_ROOT / "src" / "jvis" / "cli.py"
    assert cli.exists()
    content = cli.read_text()
    assert "def main()" in content


def test_main_module_is_runnable():
    """src/jvis/__main__.py exists and invokes main()."""
    main = PROJECT_ROOT / "src" / "jvis" / "__main__.py"
    assert main.is_file()
    content = main.read_text()
    assert "main()" in content, "__main__.py should call main()"


def test_pyproject_has_build_system():
    """pyproject.toml has [build-system] section."""
    pyproject = PROJECT_ROOT / "pyproject.toml"
    content = pyproject.read_text()
    assert "[build-system]" in content
    assert "hatchling" in content


def test_pyproject_has_scripts_entry():
    """pyproject.toml defines jvis console script."""
    pyproject = PROJECT_ROOT / "pyproject.toml"
    content = pyproject.read_text()
    assert "[project.scripts]" in content
    assert 'jvis = "jvis.cli:main"' in content


def test_pyproject_has_required_deps():
    """pyproject.toml lists core dependencies: jinja2, pyyaml, click."""
    pyproject = PROJECT_ROOT / "pyproject.toml"
    content = pyproject.read_text()
    assert "jinja2" in content
    assert "pyyaml" in content
    assert "click" in content


def test_jvis_importable():
    """The jvis package module exists and has version."""
    init_file = PROJECT_ROOT / "src" / "jvis" / "__init__.py"
    assert init_file.exists()
    content = init_file.read_text()
    assert "__version__" in content

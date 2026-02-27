"""New Project Flow Tests.

Verifies `jvis new` creates correct project structure.

Run with: pytest tests/integration/test_new_project.py -v
"""

from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent


class TestProjectStructure:
    """Tests for expected project structure components."""

    def test_jvis_config_dir_has_required_structure(self):
        """The .jvis/ directory contains required subdirectories."""
        jvis_dir = PROJECT_ROOT / ".jvis"
        assert jvis_dir.is_dir()
        for required in ("agents", "templates", "agent-engine"):
            assert (jvis_dir / required).is_dir(), f".jvis/{required}/ missing"

    def test_core_config_is_valid_yaml(self):
        """core-config.yaml exists and contains required fields."""
        import yaml

        config_path = PROJECT_ROOT / ".jvis" / "core-config.yaml"
        assert config_path.is_file(), "core-config.yaml missing"
        config = yaml.safe_load(config_path.read_text())
        assert isinstance(config, dict), "core-config.yaml must be a YAML mapping"
        assert "qa" in config, "core-config.yaml must contain qa section"

    def test_agents_directory_has_packs(self):
        """Agent directory contains the 2 expected packs."""
        agents_dir = PROJECT_ROOT / ".jvis" / "agents"
        expected_packs = {
            "core",
            "security",
        }
        found_packs = {d.name for d in agents_dir.iterdir() if d.is_dir() and not d.name.startswith(".")}
        assert expected_packs == found_packs

    def test_templates_directory_exists(self):
        """Templates directory has content."""
        templates_dir = PROJECT_ROOT / ".jvis" / "templates"
        assert templates_dir.is_dir()
        template_files = list(templates_dir.rglob("*"))
        assert len(template_files) > 50, "Expected 50+ template files"

    def test_claude_commands_directory_exists(self):
        """The .claude/commands/ directory exists with slash commands."""
        commands_dir = PROJECT_ROOT / ".claude" / "commands"
        assert commands_dir.is_dir()
        md_files = list(commands_dir.glob("*.md"))
        assert len(md_files) >= 8, f"Expected 8+ commands, found {len(md_files)}"

    def test_version_file(self):
        """Version file matches pyproject.toml."""
        version_file = PROJECT_ROOT / ".jvis" / "version"
        assert version_file.exists()
        version = version_file.read_text().strip()
        assert version == "4.5.3"

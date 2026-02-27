"""Workflow Commands Tests.

Verifies that all agent slash commands and workflow files are accessible and valid.

Run with: pytest tests/integration/test_workflow_commands.py -v
"""

from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent
COMMANDS_DIR = PROJECT_ROOT / ".claude" / "commands"
WORKFLOWS_DIR = COMMANDS_DIR / "workflows"
JOURNEY_DIR = COMMANDS_DIR / "journey"

FREE_WORKFLOWS = {"doc-update", "doc-daily", "project-resume"}

# All 10 active agents must have generated slash commands
ALL_AGENTS = {
    "dev",
    "qa",
    "architect",
    "pm",
    "sm",
    "api",
    "prisma",
    "frontend",
    "rust",
    "devsecops",
}

# Minimum content length to ensure commands are not stubs
MIN_COMMAND_LENGTH = 500


class TestFreeWorkflows:
    """Tests for free-tier workflow commands."""

    def test_workflows_directory_has_content(self):
        """The workflows directory exists and contains markdown files."""
        assert WORKFLOWS_DIR.is_dir(), f"{WORKFLOWS_DIR} does not exist"
        md_files = list(WORKFLOWS_DIR.glob("*.md"))
        assert len(md_files) >= 3, f"Expected at least 3 workflow files, found {len(md_files)}"

    def test_free_workflows_exist(self):
        """All 3 free workflows have .md files."""
        for name in FREE_WORKFLOWS:
            md_file = WORKFLOWS_DIR / f"{name}.md"
            assert md_file.exists(), f"Missing workflow: {name}.md"

    def test_free_workflows_not_empty(self):
        """Free workflow files have content."""
        for name in FREE_WORKFLOWS:
            md_file = WORKFLOWS_DIR / f"{name}.md"
            content = md_file.read_text()
            assert len(content) > 50, f"{name}.md is too short ({len(content)} chars)"


class TestJourneyCommands:
    """Tests for journey slash commands."""

    JOURNEY_COMMANDS = {"start", "status", "next", "diagnose", "complete", "gate"}

    def test_journey_directory_exists(self):
        """The journey/ subdirectory exists inside commands/."""
        assert JOURNEY_DIR.is_dir(), f"{JOURNEY_DIR} does not exist"

    def test_journey_commands_exist(self):
        """All journey commands have .md files."""
        for name in self.JOURNEY_COMMANDS:
            md_file = JOURNEY_DIR / f"{name}.md"
            assert md_file.exists(), f"Missing journey command: {name}.md"


class TestAllAgentCommands:
    """Tests for all 10 agent slash commands."""

    def test_commands_directory_has_all_agents(self):
        """The commands directory contains all 17 agent command files."""
        md_files = {p.stem for p in COMMANDS_DIR.glob("*.md")}
        missing = ALL_AGENTS - md_files
        assert not missing, f"Missing agent commands: {missing}"

    def test_all_agent_commands_have_content(self):
        """Every agent command file has substantial content (not a stub)."""
        for name in ALL_AGENTS:
            md_file = COMMANDS_DIR / f"{name}.md"
            content = md_file.read_text()
            assert len(content) > MIN_COMMAND_LENGTH, (
                f"{name}.md is too short ({len(content)} chars, min {MIN_COMMAND_LENGTH})"
            )

    def test_all_agent_commands_have_persona(self):
        """Every generated command contains a persona section."""
        for name in ALL_AGENTS:
            md_file = COMMANDS_DIR / f"{name}.md"
            content = md_file.read_text()
            assert "persona" in content.lower(), f"{name}.md missing persona section"

    def test_all_agent_commands_have_activation(self):
        """Every generated command contains activation steps."""
        for name in ALL_AGENTS:
            md_file = COMMANDS_DIR / f"{name}.md"
            content = md_file.read_text()
            assert "STEP" in content or "step" in content, f"{name}.md missing activation steps"

    def test_all_agent_commands_have_help(self):
        """Every generated command references the *help command."""
        for name in ALL_AGENTS:
            md_file = COMMANDS_DIR / f"{name}.md"
            content = md_file.read_text()
            assert "*help" in content, f"{name}.md missing *help command reference"

    def test_no_jinja2_artifacts(self):
        """No generated command contains unrendered Jinja2 markers."""
        for name in ALL_AGENTS:
            md_file = COMMANDS_DIR / f"{name}.md"
            content = md_file.read_text()
            assert "{{" not in content, f"{name}.md has unrendered Jinja2 '{{{{'"
            assert "{%" not in content, f"{name}.md has unrendered Jinja2 '{{% '"

    def test_total_agent_count(self):
        """Exactly 10 agent command files exist."""
        agent_files = [p for p in COMMANDS_DIR.glob("*.md") if p.stem in ALL_AGENTS]
        assert len(agent_files) == 10, f"Expected 10 agent commands, found {len(agent_files)}"

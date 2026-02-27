"""Agent Generation Tests.

Verifies that agent configs are valid and generate correct markdown via the engine.

Run with: pytest tests/integration/test_agent_generation.py -v
"""

from __future__ import annotations

from pathlib import Path

import jsonschema
import yaml

PROJECT_ROOT = Path(__file__).parent.parent.parent
AGENTS_DIR = PROJECT_ROOT / ".jvis" / "agents"
ENGINE_DIR = PROJECT_ROOT / ".jvis" / "agent-engine"
SCHEMA_PATH = ENGINE_DIR / "schemas" / "agent.schema.yaml"

# Dependency type → directory mapping
DEP_DIRS = {
    "tasks": PROJECT_ROOT / ".jvis" / "tasks",
    "templates": PROJECT_ROOT / ".jvis" / "templates",
    "checklists": PROJECT_ROOT / ".jvis" / "checklists",
    "data": PROJECT_ROOT / ".jvis" / "data",
}

ACTIVE_AGENTS = {
    "dev",
    "qa",
    "architect",
    "pm",
    "sm",
    "prisma",
    "frontend",
    "rust",
    "api",
    "devsecops",
}

VALID_STATUSES = {"active", "draft"}


def _get_all_agent_yamls():
    """Collect all agent YAML files."""
    return sorted(AGENTS_DIR.rglob("*.yaml"))


class TestAgentCount:
    """Verify agent count is correct."""

    def test_total_agent_count(self):
        """Total agents should be exactly 10."""
        all_yamls = _get_all_agent_yamls()
        agents = []
        for path in all_yamls:
            try:
                with open(path) as f:
                    config = yaml.safe_load(f)
                if isinstance(config, dict) and "id" in config:
                    agents.append(path)
            except (yaml.YAMLError, OSError):
                continue
        assert len(agents) == 10, f"Expected 10 agents, found {len(agents)}"


class TestAgentStatus:
    """Tests for the agent status field (active/draft)."""

    def test_all_agents_have_status(self):
        """Every agent YAML has a valid status field."""
        for path in _get_all_agent_yamls():
            try:
                with open(path) as f:
                    config = yaml.safe_load(f)
                if not isinstance(config, dict) or "id" not in config:
                    continue
                status = config.get("status")
                assert status in VALID_STATUSES, (
                    f"{path.name} has invalid status={status!r}, expected one of {VALID_STATUSES}"
                )
            except (yaml.YAMLError, OSError):
                continue

    def test_active_agent_count(self):
        """Exactly 17 agents are marked as active."""
        active = []
        for path in _get_all_agent_yamls():
            try:
                with open(path) as f:
                    config = yaml.safe_load(f)
                if isinstance(config, dict) and config.get("status") == "active":
                    active.append(path.stem)
            except (yaml.YAMLError, OSError):
                continue
        assert len(active) == 10, f"Expected 10 active agents, found {len(active)}: {sorted(active)}"

    def test_active_agents_match_expected(self):
        """The set of active agents matches the expected list."""
        active = set()
        for path in _get_all_agent_yamls():
            try:
                with open(path) as f:
                    config = yaml.safe_load(f)
                if isinstance(config, dict) and config.get("status") == "active":
                    active.add(path.stem)
            except (yaml.YAMLError, OSError):
                continue
        assert active == ACTIVE_AGENTS, f"Mismatch: extra={active - ACTIVE_AGENTS}, missing={ACTIVE_AGENTS - active}"


class TestAgentEngine:
    """Tests for the agent engine infrastructure."""

    def test_engine_importable(self):
        """engine.py is valid Python (importable syntax check)."""
        import py_compile

        engine_path = ENGINE_DIR / "engine.py"
        assert engine_path.is_file(), "engine.py missing"
        py_compile.compile(str(engine_path), doraise=True)

    def test_platform_templates_contain_jinja2(self):
        """Jinja2 platform templates exist and contain template markers."""
        templates_dir = ENGINE_DIR / "templates"
        for name in ("claude.md", "cursor.md"):
            path = templates_dir / name
            assert path.is_file(), f"{name} template missing"
            content = path.read_text()
            assert "{{" in content or "{%" in content, f"{name} should contain Jinja2 template markers"


def _load_all_agent_configs():
    """Load all agent YAML files and return list of (path, config) tuples."""
    results = []
    for path in sorted(AGENTS_DIR.rglob("*.yaml")):
        try:
            with open(path) as f:
                config = yaml.safe_load(f)
            if isinstance(config, dict) and "id" in config:
                results.append((path, config))
        except (yaml.YAMLError, OSError):
            continue
    return results


def _load_schema():
    """Load the agent JSON schema."""
    with open(SCHEMA_PATH) as f:
        return yaml.safe_load(f)


class TestAgentSchemaValidation:
    """Validate agent YAMLs against the official schema."""

    def test_agent_yaml_validates_against_schema(self):
        """Every agent YAML passes jsonschema validation against agent.schema.yaml."""
        schema = _load_schema()
        configs = _load_all_agent_configs()
        assert configs, "No agent configs found"
        for path, config in configs:
            try:
                jsonschema.validate(config, schema)
            except jsonschema.ValidationError as e:
                raise AssertionError(f"{path.name} fails schema: {e.message}") from e


    def test_agent_ids_are_unique(self):
        """No two agent YAMLs share the same agent ID."""
        configs = _load_all_agent_configs()
        seen: dict[str, str] = {}
        dupes = []
        for path, config in configs:
            aid = config["id"]
            if aid in seen:
                dupes.append(f"'{aid}' in {path.name} and {seen[aid]}")
            seen[aid] = path.name
        assert not dupes, "Duplicate agent IDs:\n" + "\n".join(dupes)

    def test_agent_writes_to_unique(self):
        """No two agents write to the same inter_agent.writes_to path."""
        configs = _load_all_agent_configs()
        seen: dict[str, str] = {}
        dupes = []
        for path, config in configs:
            writes_to = config.get("inter_agent", {}).get("writes_to")
            if not writes_to:
                continue
            if writes_to in seen:
                dupes.append(f"'{writes_to}' in {path.name} and {seen[writes_to]}")
            seen[writes_to] = path.name
        assert not dupes, "Duplicate writes_to paths:\n" + "\n".join(dupes)

    def test_agent_commands_not_empty(self):
        """Every agent has at least help, load-context, save-context, exit commands."""
        # These are common commands injected by the engine, so every agent
        # should at minimum have its own commands list (engine adds common ones).
        configs = _load_all_agent_configs()
        for path, config in configs:
            commands = config.get("commands")
            assert commands and len(commands) > 0, f"{path.name} has no agent-specific commands"

    def test_agent_handoff_agents_exist(self):
        """Every inter_agent.handoff[].agent references a valid agent ID.

        Forward references to planned-but-not-yet-created agents are allowed
        (e.g. /marketing, /dba, /infra). Only handoff refs with empty or
        whitespace-only agent IDs are flagged as invalid.
        """
        configs = _load_all_agent_configs()
        valid_ids = {config["id"] for _, config in configs}
        invalid = []
        for path, config in configs:
            handoffs = config.get("inter_agent", {}).get("handoff", [])
            for h in handoffs:
                agent_ref = h.get("agent", "")
                agent_id = agent_ref.lstrip("/")
                if not agent_id.strip():
                    invalid.append(f"{path.name}: empty handoff agent ref")
                elif agent_id in valid_ids:
                    continue  # valid reference
                # else: forward reference to future agent — allowed
        assert not invalid, "Invalid handoff agents:\n" + "\n".join(invalid)

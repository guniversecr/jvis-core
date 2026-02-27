#!/usr/bin/env python3
"""
JVIS Agent Engine
=================

Generates agent definition files from YAML configs + platform templates.

Usage:
    # Generate single agent for Claude (default)
    python engine.py generate dev

    # Generate single agent for Cursor
    python engine.py generate dev --platform cursor

    # Generate all agents for all platforms
    python engine.py generate-all --platform all

    # Validate / report / stubs / list (delegated to engine_extras)
    python engine.py validate dev
    python engine.py validate-all
    python engine.py report
    python engine.py generate-stubs
    python engine.py list
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

try:
    from jinja2 import FileSystemLoader, select_autoescape
    from jinja2.sandbox import SandboxedEnvironment
except ImportError:
    print("ERROR: jinja2 not installed. Run: pip install jinja2")
    sys.exit(1)


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
ENGINE_DIR = Path(__file__).parent
JVIS_DIR = ENGINE_DIR.parent
PROJECT_ROOT = JVIS_DIR.parent
AGENTS_DIR = JVIS_DIR / "agents"
TEMPLATES_DIR = ENGINE_DIR / "templates"
PLATFORM_DIR = JVIS_DIR / "platform"
SCHEMA_FILE = ENGINE_DIR / "schemas" / "agent.schema.yaml"

# Dependency directories
DEPS_DIRS = {
    "checklists": JVIS_DIR / "checklists",
    "tasks": JVIS_DIR / "tasks",
    "templates": JVIS_DIR / "templates",
    "data": JVIS_DIR / "data",
}

# Packs structure (ordered by priority)
PACKS = [
    "core",
    "data",
    "security",
    "devops",
    "cloud",
    "mobile",
    "integrations",
]

# ---------------------------------------------------------------------------
# Platform configuration
# ---------------------------------------------------------------------------
PLATFORMS: dict[str, dict[str, Any]] = {
    "claude": {
        "template": "claude.md",
        "output_dir": PROJECT_ROOT / ".claude" / "commands",
        "extension": ".md",
    },
    "cursor": {
        "template": "cursor.md",
        "output_dir": PROJECT_ROOT / ".cursor" / "rules",
        "extension": ".mdc",
    },
}


# ---------------------------------------------------------------------------
# DependencyStatus
# ---------------------------------------------------------------------------
@dataclass
class DependencyStatus:
    """Status of an agent's dependencies."""
    agent_id: str
    pack: str
    total: int = 0
    missing: int = 0
    missing_files: list[str] = field(default_factory=list)

    @property
    def completeness(self) -> float:
        if self.total == 0:
            return 100.0
        return ((self.total - self.missing) / self.total) * 100

    @property
    def status_icon(self) -> str:
        pct = self.completeness
        if pct == 100:
            return "✅"
        elif pct >= 80:
            return "🟡"
        elif pct >= 50:
            return "🟠"
        else:
            return "🔴"


# ---------------------------------------------------------------------------
# Jinja2 helpers
# ---------------------------------------------------------------------------
def toyaml_filter(value: Any, default_flow_style: bool = False) -> str:
    """Jinja2 filter to convert Python objects to YAML."""
    result: str = yaml.dump(value, default_flow_style=default_flow_style).strip()
    return result


def setup_jinja_env() -> SandboxedEnvironment:
    """Configure Jinja2 environment with templates/ directory."""
    env = SandboxedEnvironment(
        loader=FileSystemLoader(TEMPLATES_DIR),
        autoescape=select_autoescape(),
        trim_blocks=False,
        lstrip_blocks=False,
    )
    env.filters["toyaml"] = toyaml_filter
    return env


# ---------------------------------------------------------------------------
# Agent config loading
# ---------------------------------------------------------------------------
def load_agent_config(agent_id: str) -> dict[str, Any] | None:
    """Load agent configuration from YAML file."""
    for pack in PACKS:
        config_path = AGENTS_DIR / pack / f"{agent_id}.yaml"
        if config_path.exists():
            with open(config_path) as f:
                config: dict[str, Any] = yaml.safe_load(f)
                config["pack"] = pack
                return config

    # Legacy: check root agents dir
    config_path = AGENTS_DIR / f"{agent_id}.yaml"
    if config_path.exists():
        with open(config_path) as f:
            result: dict[str, Any] = yaml.safe_load(f)
            return result

    return None


def find_all_agents() -> list[tuple[str, str, dict[str, Any]]]:
    """Find all agent configs. Returns list of (pack, agent_id, config)."""
    agents = []

    for pack in PACKS:
        pack_dir = AGENTS_DIR / pack
        if pack_dir.exists():
            for config_file in pack_dir.glob("*.yaml"):
                agent_id = config_file.stem
                with open(config_file) as f:
                    config = yaml.safe_load(f)
                    config["pack"] = pack
                    agents.append((pack, agent_id, config))

    return sorted(agents, key=lambda x: (PACKS.index(x[0]), x[1]))


# ---------------------------------------------------------------------------
# Dependency validation
# ---------------------------------------------------------------------------
def validate_dependencies(config: dict[str, Any]) -> DependencyStatus:
    """Validate that all dependencies exist. Returns status object."""
    agent_id = config.get("id", "unknown")
    pack = config.get("pack", "unknown")

    status = DependencyStatus(agent_id=agent_id, pack=pack)
    deps = config.get("dependencies", {})

    for dep_type, dep_dir in DEPS_DIRS.items():
        for dep_file in deps.get(dep_type, []):
            status.total += 1
            full_path = dep_dir / dep_file
            if not full_path.exists():
                status.missing += 1
                status.missing_files.append(f"{dep_type}/{dep_file}")

    return status


# ---------------------------------------------------------------------------
# Extras file loading
# ---------------------------------------------------------------------------
def load_extras(agent_id: str, platform: str) -> str:
    """Load platform-specific extras file content if it exists."""
    extras_path = PLATFORM_DIR / platform / f"{agent_id}-extras.md"
    if extras_path.exists():
        return extras_path.read_text()
    return ""


# ---------------------------------------------------------------------------
# Generation
# ---------------------------------------------------------------------------
def generate_agent(
    agent_id: str,
    platform: str = "claude",
    strict: bool = False,
) -> Path | None:
    """Generate agent output for a specific platform."""
    config = load_agent_config(agent_id)
    if not config:
        print(f"ERROR: Agent config not found: {agent_id}")
        return None

    if platform not in PLATFORMS:
        print(f"ERROR: Unknown platform: {platform}. Choose from: {list(PLATFORMS.keys())}")
        return None

    # Validate dependencies
    dep_status = validate_dependencies(config)
    if dep_status.missing > 0:
        if strict:
            print(f"ERROR: {agent_id} has {dep_status.missing} missing dependencies:")
            for missing_file in dep_status.missing_files[:5]:
                print(f"  - {missing_file}")
            if len(dep_status.missing_files) > 5:
                print(f"  ... and {len(dep_status.missing_files) - 5} more")
            return None
        else:
            print(f"  WARN: {agent_id} — {dep_status.missing}/{dep_status.total} dependencies missing")

    # Setup Jinja2
    env = setup_jinja_env()
    plat_cfg = PLATFORMS[platform]
    template = env.get_template(plat_cfg["template"])

    # Set config defaults
    config.setdefault("activation_extras", [])
    config.setdefault("icon", "🤖")
    config.setdefault("customization", None)
    config.setdefault("inter_agent", {})
    config.setdefault("dependencies", {})
    config.setdefault("extended_docs", "")
    config.setdefault("platform_meta", {})

    # Load extras content
    extras_content = load_extras(agent_id, platform)

    # Platform-specific metadata — extract before passing config to template
    plat_meta = config.pop("platform_meta", {}).get(platform, {})

    # Render template
    output = template.render(
        extras_content=extras_content,
        platform_meta=plat_meta,
        **config,
    ).lstrip('\n')

    # Write to platform output directory
    output_dir = plat_cfg["output_dir"]
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{agent_id}{plat_cfg['extension']}"

    with open(output_path, "w") as fh:
        fh.write(output)

    return output_path


def generate_all(
    platform: str = "claude",
    strict: bool = False,
    include_drafts: bool = False,
) -> list[Path]:
    """Generate all agents for a given platform (or 'all').

    By default only agents with ``status: active`` are generated.
    Pass *include_drafts=True* (``--include-drafts``) to generate all agents.

    Note: The output directories (.claude/commands/, .cursor/commands/) may
    contain static command files (e.g. tutorial.md, journey/, workflows/) that
    are NOT generated from agent YAML configs. This function only writes files
    matching agent IDs — it never deletes the output directory. Keep this
    invariant if refactoring.
    """
    platforms = list(PLATFORMS.keys()) if platform == "all" else [platform]
    agents = find_all_agents()

    if not include_drafts:
        skipped = [(p, a, c) for p, a, c in agents if c.get("status", "draft") == "draft"]
        agents = [(p, a, c) for p, a, c in agents if c.get("status", "draft") != "draft"]
        if skipped:
            print(f"Skipping {len(skipped)} draft agents (use --include-drafts to include them)")

    generated = []
    failed = []

    for plat in platforms:
        if plat not in PLATFORMS:
            print(f"ERROR: Unknown platform: {plat}")
            continue

        print(f"\n{'='*50}")
        print(f"Generating for: {plat}")
        print(f"{'='*50}")

        for pack, agent_id, config in agents:
            result = generate_agent(agent_id, platform=plat, strict=strict)
            if result:
                generated.append(result)
                dep_status = validate_dependencies(config)
                icon = dep_status.status_icon
                print(f"  {icon} {agent_id} ({pack}) - {dep_status.completeness:.0f}% deps")
            else:
                failed.append(agent_id)
                print(f"  ✗ {agent_id} - FAILED")

    if failed and strict:
        print(f"\n❌ {len(failed)} agents failed strict validation")

    return generated


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(
        description="JVIS Agent Engine - Generate agent definitions for multiple platforms",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python engine.py generate dev                    # Generate for Claude (default)
  python engine.py generate dev --platform cursor  # Generate for Cursor
  python engine.py generate-all --platform all     # Generate all agents, all platforms
  python engine.py validate dev                    # Validate single agent
  python engine.py validate-all                    # Validate all agents
  python engine.py report                          # Show completeness report
  python engine.py report --json                   # JSON format report
  python engine.py generate-stubs                  # Create missing dependency files
  python engine.py generate-stubs --dry-run        # Preview without creating
        """
    )
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # generate
    gen_parser = subparsers.add_parser("generate", help="Generate single agent")
    gen_parser.add_argument("agent_id", help="Agent ID to generate")
    gen_parser.add_argument("--platform", "-p", default="claude",
                            choices=["claude", "cursor", "all"],
                            help="Target platform (default: claude)")
    gen_parser.add_argument("--strict", action="store_true",
                            help="Fail on missing dependencies")

    # generate-all
    genall_parser = subparsers.add_parser("generate-all", help="Generate all agents")
    genall_parser.add_argument("--platform", "-p", default="claude",
                               choices=["claude", "cursor", "all"],
                               help="Target platform (default: claude)")
    genall_parser.add_argument("--strict", action="store_true",
                               help="Fail on missing dependencies")
    genall_parser.add_argument("--include-drafts", action="store_true",
                               help="Include draft agents in generation")

    # validate
    val_parser = subparsers.add_parser("validate", help="Validate agent config")
    val_parser.add_argument("agent_id", help="Agent ID to validate")
    val_parser.add_argument("--no-deps", action="store_true",
                            help="Skip dependency check")

    # validate-all
    subparsers.add_parser("validate-all", help="Validate all agents")

    # list
    list_parser = subparsers.add_parser("list", help="List agents")
    list_parser.add_argument("--pack", choices=PACKS, help="Filter by pack")

    # report
    report_parser = subparsers.add_parser("report", help="Show completeness report")
    report_parser.add_argument("--json", action="store_true",
                               help="Output as JSON")

    # generate-stubs
    stubs_parser = subparsers.add_parser("generate-stubs",
                                          help="Generate stub files for missing dependencies")
    stubs_parser.add_argument("--dry-run", action="store_true",
                              help="Preview without creating files")

    args = parser.parse_args()

    if args.command == "generate":
        platforms = list(PLATFORMS.keys()) if args.platform == "all" else [args.platform]
        for plat in platforms:
            result = generate_agent(args.agent_id, platform=plat, strict=args.strict)
            if result:
                print(f"Generated: {result}")
            else:
                sys.exit(1)

    elif args.command == "generate-all":
        results = generate_all(
            platform=args.platform,
            strict=args.strict,
            include_drafts=args.include_drafts,
        )
        print(f"\nGenerated {len(results)} files")
        if args.strict and len(results) < len(find_all_agents()):
            sys.exit(1)

    elif args.command in ("validate", "validate-all", "report",
                          "generate-stubs", "list"):
        # Delegate to engine_extras
        from engine_extras import (
            generate_report,
            generate_stubs,
            list_agents,
            validate_all,
            validate_config,
        )

        if args.command == "validate":
            check_deps = not args.no_deps
            if not validate_config(args.agent_id, check_deps=check_deps):
                sys.exit(1)

        elif args.command == "validate-all":
            passed, failed = validate_all()
            print(f"\n{passed} passed, {failed} failed")
            if failed > 0:
                sys.exit(1)

        elif args.command == "list":
            list_agents(pack=args.pack)

        elif args.command == "report":
            output_format = "json" if args.json else "text"
            generate_report(output_format)

        elif args.command == "generate-stubs":
            count = generate_stubs(dry_run=args.dry_run)
            action = "Would create" if args.dry_run else "Created"
            print(f"\n{action} {count} stub files")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()

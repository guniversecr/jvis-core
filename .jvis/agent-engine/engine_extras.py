"""
JVIS Agent Engine - Extras
==========================

Reporting, validation, and stub generation utilities.
Split from engine.py to keep the core generation pipeline lean.

Usage:
    These functions are called from engine.py CLI commands:
    - validate, validate-all
    - report
    - generate-stubs
    - list
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml
from jsonschema import ValidationError, validate

from engine import (
    DEPS_DIRS,
    PACKS,
    SCHEMA_FILE,
    find_all_agents,
    load_agent_config,
    validate_dependencies,
)

_SCHEMA: dict[str, Any] | None = None


def _load_schema() -> dict[str, Any]:
    """Load and cache the agent schema from YAML."""
    global _SCHEMA  # noqa: PLW0603
    if _SCHEMA is None:
        _SCHEMA = yaml.safe_load(SCHEMA_FILE.read_text())
    return _SCHEMA


def validate_config(agent_id: str, check_deps: bool = True) -> bool:
    """Validate agent config against agent.schema.yaml (SSOT)."""
    config = load_agent_config(agent_id)
    if not config:
        print(f"ERROR: Agent config not found: {agent_id}")
        return False

    errors: list[str] = []

    # Schema validation — required fields, enums, types, nested objects
    schema = _load_schema()
    try:
        validate(instance=config, schema=schema)
    except ValidationError as exc:
        errors.append(exc.message)

    # Dependency validation (file-system check, not expressible in JSON Schema)
    if check_deps:
        dep_status = validate_dependencies(config)
        if dep_status.missing > 0:
            errors.append(f"{dep_status.missing}/{dep_status.total} dependencies missing")

    if errors:
        print(f"✗ {agent_id}:")
        for err in errors:
            print(f"    - {err}")
        return False

    dep_status = validate_dependencies(config)
    print(f"✓ {agent_id} ({dep_status.completeness:.0f}% complete)")
    return True


def validate_all() -> tuple[int, int]:
    """Validate all agents. Returns (passed, failed) counts."""
    agents = find_all_agents()
    passed = 0
    failed = 0

    for _pack, agent_id, _ in agents:
        if validate_config(agent_id, check_deps=True):
            passed += 1
        else:
            failed += 1

    return passed, failed


def generate_report(output_format: str = "text") -> None:
    """Generate completeness report for all agents."""
    agents = find_all_agents()
    statuses = []

    for _pack, _agent_id, config in agents:
        status = validate_dependencies(config)
        statuses.append(status)

    # Sort by completeness (lowest first for attention)
    statuses.sort(key=lambda s: s.completeness)

    if output_format == "json":
        data = {
            "summary": {
                "total_agents": len(statuses),
                "fully_complete": sum(1 for s in statuses if s.completeness == 100),
                "average_completeness": sum(s.completeness for s in statuses) / len(statuses) if statuses else 0,
            },
            "agents": [
                {
                    "id": s.agent_id,
                    "pack": s.pack,
                    "completeness": s.completeness,
                    "total_deps": s.total,
                    "missing_deps": s.missing,
                    "missing_files": s.missing_files,
                }
                for s in statuses
            ]
        }
        print(json.dumps(data, indent=2))
        return

    # Text format
    print("=" * 70)
    print("JVIS AGENT COMPLETENESS REPORT")
    print("=" * 70)

    # Summary
    total = len(statuses)
    complete = sum(1 for s in statuses if s.completeness == 100)
    avg = sum(s.completeness for s in statuses) / total if total else 0

    print("\nSummary:")
    print(f"  Total agents: {total}")
    print(f"  Fully complete: {complete} ({complete/total*100:.1f}%)")
    print(f"  Average completeness: {avg:.1f}%")

    # By pack
    print("\nBy Pack:")
    for pack in PACKS:
        pack_agents = [s for s in statuses if s.pack == pack]
        if pack_agents:
            pack_avg = sum(s.completeness for s in pack_agents) / len(pack_agents)
            icon = "✅" if pack_avg == 100 else "🟡" if pack_avg >= 80 else "🟠" if pack_avg >= 50 else "🔴"
            print(f"  {icon} {pack}: {len(pack_agents)} agents, {pack_avg:.1f}% avg")

    # Agents needing attention (below 100%)
    incomplete = [s for s in statuses if s.completeness < 100]
    if incomplete:
        print(f"\n{'=' * 70}")
        print("AGENTS NEEDING ATTENTION (sorted by priority)")
        print("=" * 70)

        for s in incomplete:
            print(f"  {s.status_icon} {s.agent_id:<20} {s.completeness:5.1f}% ({s.total - s.missing}/{s.total} deps)")

    # Missing files summary
    all_missing: dict[str, set[str]] = {}
    for s in statuses:
        for f in s.missing_files:
            dep_type = f.split("/")[0]
            all_missing.setdefault(dep_type, set()).add(f)

    if all_missing:
        print(f"\n{'=' * 70}")
        print("MISSING DEPENDENCIES BY TYPE")
        print("=" * 70)
        for dep_type in ["templates", "checklists", "tasks", "data"]:
            if dep_type in all_missing:
                count = len(all_missing[dep_type])
                print(f"\n{dep_type}: {count} missing")
                for f in sorted(all_missing[dep_type])[:10]:
                    print(f"  - {f}")
                if count > 10:
                    print(f"  ... and {count - 10} more")


def generate_stubs(dry_run: bool = False) -> int:
    """Generate stub files for all missing dependencies."""
    agents = find_all_agents()
    all_missing: dict[str, set[str]] = {}

    # Collect all missing files
    for _, _, config in agents:
        status = validate_dependencies(config)
        for f in status.missing_files:
            dep_type = f.split("/")[0]
            dep_path = "/".join(f.split("/")[1:])
            all_missing.setdefault(dep_type, set()).add(dep_path)

    created = 0

    for dep_type, files in all_missing.items():
        dep_dir = DEPS_DIRS.get(dep_type)
        if not dep_dir:
            continue

        for file_path in sorted(files):
            full_path = dep_dir / file_path

            if dry_run:
                print(f"  Would create: {full_path}")
                created += 1
                continue

            # Create directory if needed
            full_path.parent.mkdir(parents=True, exist_ok=True)

            # Determine stub content based on file type
            ext = full_path.suffix.lower()
            stub_content = generate_stub_content(file_path, dep_type, ext)

            # Write stub file
            with open(full_path, "w") as fh:
                fh.write(stub_content)

            print(f"  ✓ Created: {full_path}")
            created += 1

    return created


def _stub_markdown(name: str, dep_type: str) -> str:
    return f"""# {name.replace('-', ' ').replace('_', ' ').title()}

> TODO: Implement {name}

## Overview

This {dep_type.rstrip('s')} is pending implementation.

## Contents

<!-- Add content here -->

---
*Generated stub - needs implementation*
"""


def _stub_yaml(name: str, dep_type: str) -> str:
    return f"""# {name}
# TODO: Implement {name}

# This {dep_type.rstrip('s')} is pending implementation.
# Add YAML content below:

metadata:
  name: {name}
  status: stub
  todo: true

# Add fields here
"""


def _stub_json(name: str, dep_type: str) -> str:
    return f"""{{"_comment": "TODO: Implement {name}",
  "metadata": {{
    "name": "{name}",
    "status": "stub"
  }}
}}
"""


def _stub_python(name: str, dep_type: str) -> str:
    return f'''"""
{name}

TODO: Implement {name}
"""

# This {dep_type.rstrip('s')} is pending implementation.

def main():
    raise NotImplementedError("{name} not yet implemented")


if __name__ == "__main__":
    main()
'''


def _stub_javascript(name: str, dep_type: str) -> str:
    return f"""// {name}
// TODO: Implement {name}

// This {dep_type.rstrip('s')} is pending implementation.

export default function {name.replace('-', '_').replace('.', '_')}() {{
  throw new Error('{name} not yet implemented');
}}
"""


def _stub_terraform(name: str, dep_type: str) -> str:
    return f"""# {name}
# TODO: Implement {name}

# This Terraform template is pending implementation.

# Add resources here
"""


def _stub_rust(name: str, dep_type: str) -> str:
    return f"""// {name}
// TODO: Implement {name}

// This Rust template is pending implementation.

pub fn main() {{
    todo!("{name} not yet implemented");
}}
"""


def _stub_kotlin(name: str, dep_type: str) -> str:
    return f"""// {name}
// TODO: Implement {name}

// This Kotlin template is pending implementation.

fun main() {{
    TODO("{name} not yet implemented")
}}
"""


def _stub_swift(name: str, dep_type: str) -> str:
    return f"""// {name}
// TODO: Implement {name}

// This Swift template is pending implementation.

import Foundation

func main() {{
    fatalError("{name} not yet implemented")
}}
"""


def _stub_dart(name: str, dep_type: str) -> str:
    return f"""// {name}
// TODO: Implement {name}

// This Flutter/Dart template is pending implementation.

void main() {{
  throw UnimplementedError('{name} not yet implemented');
}}
"""


def _stub_csharp(name: str, dep_type: str) -> str:
    return f"""// {name}
// TODO: Implement {name}

// This C# template is pending implementation.

using System;

public class {name.replace('-', '_')} {{
    public static void Main() {{
        throw new NotImplementedException("{name} not yet implemented");
    }}
}}
"""


def _stub_liquid(name: str, dep_type: str) -> str:
    return f"""{{% comment %}}
{name}
TODO: Implement {name}
{{% endcomment %}}

<!-- This Shopify template is pending implementation -->
"""


def _stub_config(name: str, dep_type: str) -> str:
    return f"""# {name}
# TODO: Implement {name}

# This configuration template is pending implementation.
"""


def _stub_dockerfile(name: str, dep_type: str) -> str:
    return f"""# {name}
# TODO: Implement {name}

# This Dockerfile template is pending implementation.

FROM scratch
# Add Dockerfile instructions here
"""


def _stub_generic(name: str, dep_type: str, ext: str = "") -> str:
    return f"""# {name}
# TODO: Implement {name}

# This {dep_type.rstrip('s')} is pending implementation.
# File type: {ext or 'unknown'}
"""


_STUB_GENERATORS: dict[str, Any] = {
    ".md": _stub_markdown,
    ".yaml": _stub_yaml,
    ".yml": _stub_yaml,
    ".json": _stub_json,
    ".py": _stub_python,
    ".ts": _stub_javascript,
    ".tsx": _stub_javascript,
    ".js": _stub_javascript,
    ".jsx": _stub_javascript,
    ".tf": _stub_terraform,
    ".rs": _stub_rust,
    ".kt": _stub_kotlin,
    ".swift": _stub_swift,
    ".dart": _stub_dart,
    ".cs": _stub_csharp,
    ".liquid": _stub_liquid,
    ".conf": _stub_config,
}


def _resolve_generator(file_path: str, ext: str) -> Any:
    """Return the appropriate stub generator for *file_path*."""
    if ext in (".dockerfile", "") and "dockerfile" in file_path.lower():
        return _stub_dockerfile
    return _STUB_GENERATORS.get(ext)


def generate_stub_content(file_path: str, dep_type: str, ext: str) -> str:
    """Generate appropriate stub content for a file."""
    name = Path(file_path).stem
    generator = _resolve_generator(file_path, ext)
    if generator is not None:
        return generator(name, dep_type)
    return _stub_generic(name, dep_type, ext)


def list_agents(pack: str | None = None) -> None:
    """List all agents, optionally filtered by pack."""
    agents = find_all_agents()

    if pack:
        agents = [(p, a, c) for p, a, c in agents if p == pack]

    if not agents:
        print("No agents found matching criteria.")
        return

    # Group by pack
    by_pack: dict[str, list] = {}
    for p, agent_id, config in agents:
        by_pack.setdefault(p, []).append((agent_id, config))

    for pack_name in PACKS:
        if pack_name not in by_pack:
            continue
        pack_agents = by_pack[pack_name]
        print(f"\n{pack_name.upper()} ({len(pack_agents)} agents)")
        print("-" * 40)
        for agent_id, config in pack_agents:
            status_badge = "🟢" if config.get("status", "draft") == "active" else "⚪"
            dep_status = validate_dependencies(config)
            dep_icon = dep_status.status_icon
            name = config.get("name", "Unknown")
            title = config.get("title", "")
            print(f"  {status_badge}{dep_icon} {agent_id}: {name} - {title}")

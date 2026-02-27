"""Stack registry — discover stacks from data/stacks/ manifests."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

from jvis.utils.paths import get_data_dir

logger = logging.getLogger(__name__)


@dataclass
class StackInfo:
    """Metadata for a single stack."""

    id: str
    name: str
    description: str
    type: str  # backend, frontend, mobile
    language: str
    framework: str
    directory: Path | None = None  # path to the stack data dir (manifest + files/)
    agents: list[str] = field(default_factory=list)
    requires_database: bool = False
    dev_command: str = ""
    dev_port: int = 8000  # Default fallback; most backend frameworks use 8000 (uvicorn, Django, Flask)
    getting_started: dict[str, Any] = field(default_factory=dict)

    @property
    def display(self) -> str:
        return f"{self.name} — {self.description}"


@lru_cache(maxsize=1)
def discover_stacks() -> dict[str, StackInfo]:
    """Find all stacks from data/stacks/*/manifest.yaml. Returns {id: StackInfo}."""
    stacks_dir = _get_stacks_dir()
    if not stacks_dir.is_dir():
        return {}

    result: dict[str, StackInfo] = {}
    # sorted() ensures deterministic discovery order across platforms.
    # Catch broad exceptions per manifest so one broken stack doesn't block all others.
    for manifest_path in sorted(stacks_dir.glob("*/manifest.yaml")):
        try:
            info = _load_manifest(manifest_path)
            result[info.id] = info
        except (yaml.YAMLError, KeyError, OSError) as exc:
            logger.warning("Skipping invalid manifest: %s (%s)", manifest_path, exc)
            continue

    return result


def get_stacks_by_type(stack_type: str) -> dict[str, StackInfo]:
    """Return stacks filtered by type (backend, frontend, mobile)."""
    return {k: v for k, v in discover_stacks().items() if v.type == stack_type}


def get_stack(stack_id: str) -> StackInfo | None:
    """Return a single stack by ID, or None."""
    return discover_stacks().get(stack_id)


def _get_stacks_dir() -> Path:
    """Locate the stacks data directory."""
    return get_data_dir() / "stacks"


def _load_manifest(path: Path) -> StackInfo:
    """Parse a manifest.yaml into StackInfo."""
    with open(path) as f:
        raw = yaml.safe_load(f)

    return StackInfo(
        id=raw["id"],
        name=raw["name"],
        description=raw.get("description", ""),
        type=raw.get("type", "backend"),
        language=raw.get("language", ""),
        framework=raw.get("framework", ""),
        directory=path.parent,
        agents=raw.get("agents", []),
        requires_database=raw.get("requires_database", False),
        dev_command=raw.get("dev_command", ""),
        dev_port=raw.get("dev_port", 8000),
        getting_started=raw.get("getting_started", {}),
    )

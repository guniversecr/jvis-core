"""Stack runner — load a stack manifest and render its template files into a project."""

from __future__ import annotations

import logging
from datetime import date
from pathlib import Path
from typing import Any

import yaml
from jinja2.sandbox import SandboxedEnvironment

from jvis.stacks.registry import StackInfo
from jvis.utils.fs import copy_file, mkdir_p, write_file

logger = logging.getLogger(__name__)


def run_stack(
    stack: StackInfo,
    target_dir: Path,
    project_name: str,
    project_description: str = "",
    database: str = "",
) -> None:
    """Apply a stack manifest: create directories and render template files.

    Template variables available in .j2 files:
      - project_name, project_description, database_type, date
    """
    if stack.directory is None:
        logger.warning("Stack %s has no directory, skipping scaffold", stack.id)
        return
    manifest = _load_full_manifest(stack.directory / "manifest.yaml")
    ctx = _build_context(project_name, project_description, database)
    env = SandboxedEnvironment()

    # Create directories from manifest
    for dirname in manifest.get("directories", []):
        mkdir_p(target_dir / dirname)

    # Process files
    files_dir = stack.directory / "files"
    for file_entry in manifest.get("files", []):
        _process_file(file_entry, files_dir, target_dir, ctx, env)


def _load_full_manifest(path: Path) -> dict[str, Any]:
    with open(path) as f:
        return yaml.safe_load(f) or {}


def _build_context(project_name: str, description: str, database: str) -> dict[str, str]:
    return {
        "project_name": project_name,
        "project_description": description or f"{project_name} project",
        "database_type": database or "postgresql",
        "date": date.today().isoformat(),
    }


def _process_file(
    entry: dict[str, str] | str,
    files_dir: Path,
    target_dir: Path,
    ctx: dict[str, str],
    env: SandboxedEnvironment | None = None,
) -> None:
    """Process a single file entry from the manifest.

    Entry can be:
      - a string: "path/to/file" (copy as-is from files/)
      - a dict: {"src": "template.j2", "dst": "output.py"} (render Jinja2)
      - a dict: {"src": "file.txt", "dst": "file.txt"} (copy)
    """
    if isinstance(entry, str):
        src_name = entry
        dst_name = entry
    else:
        src_name = entry["src"]
        dst_name = entry.get("dst", src_name)

    # Strip .j2 suffix so "main.py.j2" renders to "main.py" in the output.
    # Convention: .j2 files are Jinja2 templates; non-.j2 files are copied verbatim.
    if dst_name.endswith(".j2"):
        dst_name = dst_name[:-3]

    src_path = files_dir / src_name
    dst_path = target_dir / dst_name

    if not src_path.is_file():
        logger.warning("Template file not found, skipping: %s", src_path)
        return

    if src_name.endswith(".j2"):
        # Render Jinja2 template
        template_text = src_path.read_text(encoding="utf-8")
        if env is None:
            env = SandboxedEnvironment()
        rendered = env.from_string(template_text).render(**ctx)
        write_file(dst_path, rendered)
    else:
        # Copy as-is
        copy_file(src_path, dst_path)

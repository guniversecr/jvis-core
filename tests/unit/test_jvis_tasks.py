"""Task File Validation Tests.

Validates the structural integrity of .jvis/tasks/ markdown files:
non-empty, H1 header, structure sections, minimum count, valid filenames.

Run with: pytest tests/unit/test_jvis_tasks.py -v
"""

from __future__ import annotations

import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent
TASKS_DIR = PROJECT_ROOT / ".jvis" / "tasks"


def _get_all_task_files():
    """Collect all .md task files (excluding README)."""
    return sorted(p for p in TASKS_DIR.rglob("*.md") if p.is_file() and p.name != "README.md")


def _strip_frontmatter(content: str) -> str:
    """Strip optional HTML comments and YAML front matter from content.

    Task files may start with:
    - <!-- Powered by JVIS --> comment
    - YAML front matter block (## heading + key: value before ---)
    """
    # Strip leading HTML comments
    content = re.sub(r"^<!--.*?-->\s*", "", content.lstrip(), flags=re.DOTALL)
    # Strip YAML front matter: starts with ## or key: before first ---
    if "---" in content:
        before_sep, _, after_sep = content.partition("---")
        # If before separator has no H1 but after does, it's front matter
        if "# " not in before_sep.split("\n")[0] or before_sep.lstrip().startswith("##"):
            after_stripped = after_sep.lstrip()
            if after_stripped.startswith("# "):
                return after_stripped
    return content.lstrip()


class TestTaskFileIntegrity:
    """Task file structural validation."""

    def test_task_files_not_empty(self):
        """No task file is 0 bytes or whitespace-only."""
        tasks = _get_all_task_files()
        assert tasks, "No task files found"
        empty = []
        for path in tasks:
            content = path.read_text(encoding="utf-8", errors="replace")
            if not content.strip():
                empty.append(path.name)
        assert not empty, "Empty task files:\n" + "\n".join(empty)

    def test_task_files_have_header(self):
        """Every .md task has an H1 heading (# Title)."""
        tasks = _get_all_task_files()
        no_header = []
        for path in tasks:
            content = path.read_text(encoding="utf-8", errors="replace")
            body = _strip_frontmatter(content)
            if not body.startswith("# "):
                no_header.append(path.name)
        assert not no_header, "Tasks missing H1 header:\n" + "\n".join(no_header)

    def test_task_files_have_structure(self):
        """Every task has at least one ## section heading."""
        tasks = _get_all_task_files()
        no_sections = []
        for path in tasks:
            content = path.read_text(encoding="utf-8", errors="replace")
            # Look for any ## heading (Purpose, Objective, Overview, Steps, etc.)
            if not re.search(r"^## ", content, re.MULTILINE):
                no_sections.append(path.name)
        assert not no_sections, "Tasks with no ## sections:\n" + "\n".join(no_sections)

    def test_task_count_minimum(self):
        """At least 200 task files exist (catches accidental mass deletion)."""
        tasks = _get_all_task_files()
        assert len(tasks) >= 200, f"Expected >=200 tasks, found {len(tasks)}"

    def test_task_filenames_valid(self):
        """All task filenames are lowercase, use hyphens (no spaces, no uppercase)."""
        tasks = _get_all_task_files()
        invalid = []
        for path in tasks:
            name = path.stem  # without .md
            if name != name.lower():
                invalid.append(f"{path.name}: contains uppercase")
            elif " " in name:
                invalid.append(f"{path.name}: contains spaces")
            elif not re.match(r"^[a-z0-9][a-z0-9-]*$", name):
                invalid.append(f"{path.name}: invalid characters")
        assert not invalid, "Invalid task filenames:\n" + "\n".join(invalid)

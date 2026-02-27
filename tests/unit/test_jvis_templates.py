"""Template Validation Tests.

Validates the structural integrity of .jvis/templates/ files:
YAML parsing, required keys, unique IDs, non-empty, Jinja2 balance.

Run with: pytest tests/unit/test_jvis_templates.py -v
"""

from __future__ import annotations

from pathlib import Path

import yaml

PROJECT_ROOT = Path(__file__).parent.parent.parent
TEMPLATES_DIR = PROJECT_ROOT / ".jvis" / "templates"


def _get_all_template_files():
    """Collect all template files (excluding README)."""
    return sorted(p for p in TEMPLATES_DIR.rglob("*") if p.is_file() and p.name != "README.md")


def _get_yaml_template_files():
    """Collect only .yaml/.yml template files."""
    return sorted(
        p for p in TEMPLATES_DIR.rglob("*") if p.is_file() and p.suffix in (".yaml", ".yml") and p.name != "README.md"
    )


def _parse_yaml_segments(path):
    """Parse YAML template, handling trailing markdown after ---.

    Template files use the format:
      [comments] --- [YAML body] --- [trailing markdown]
    The trailing markdown is not valid YAML. We split by '---' and
    parse each segment individually, returning parsed dicts.
    """
    text = path.read_text(encoding="utf-8", errors="replace")
    segments = text.split("\n---\n")
    parsed = []
    for seg in segments:
        seg = seg.strip()
        if not seg:
            continue
        try:
            doc = yaml.safe_load(seg)
            if isinstance(doc, dict):
                parsed.append(doc)
        except yaml.YAMLError:
            continue
    return parsed


class TestTemplateYamlParsing:
    """YAML template structural validation."""

    def test_yaml_templates_parse(self):
        """All YAML template files have at least one parseable YAML segment."""
        yaml_files = _get_yaml_template_files()
        assert yaml_files, "No YAML templates found"
        errors = []
        for path in yaml_files:
            docs = _parse_yaml_segments(path)
            if not docs:
                errors.append(str(path.relative_to(PROJECT_ROOT)))
        assert not errors, "YAML files with no parseable segments:\n" + "\n".join(errors)

    def test_yaml_templates_have_required_keys(self):
        """YAML templates with template: root have name and version."""
        yaml_files = _get_yaml_template_files()
        missing = []
        for path in yaml_files:
            for data in _parse_yaml_segments(path):
                tmpl = data.get("template")
                if not isinstance(tmpl, dict):
                    continue
                required = {"name", "version"}
                absent = required - set(tmpl.keys())
                if absent:
                    missing.append(f"{path.relative_to(PROJECT_ROOT)}: missing {absent}")
        assert not missing, "Templates missing required keys:\n" + "\n".join(missing)

    def test_template_ids_unique(self):
        """No duplicate template.id values across all YAML templates."""
        yaml_files = _get_yaml_template_files()
        seen: dict[str, str] = {}
        dupes = []
        for path in yaml_files:
            for data in _parse_yaml_segments(path):
                tmpl = data.get("template")
                if not isinstance(tmpl, dict):
                    continue
                tid = tmpl.get("id")
                if not tid:
                    continue
                rel = str(path.relative_to(PROJECT_ROOT))
                if tid in seen:
                    dupes.append(f"'{tid}' in {rel} and {seen[tid]}")
                seen[tid] = rel
        assert not dupes, "Duplicate template IDs:\n" + "\n".join(dupes)


class TestTemplateIntegrity:
    """Non-YAML and cross-format template checks."""

    def test_no_empty_template_files(self):
        """No template file is 0 bytes or whitespace-only."""
        all_files = _get_all_template_files()
        empty = []
        for path in all_files:
            content = path.read_text(encoding="utf-8", errors="replace")
            if not content.strip():
                empty.append(str(path.relative_to(PROJECT_ROOT)))
        assert not empty, "Empty template files:\n" + "\n".join(empty)

    def test_jinja2_templates_balanced(self):
        """Files containing {{ have matching }}."""
        all_files = _get_all_template_files()
        unbalanced = []
        for path in all_files:
            content = path.read_text(encoding="utf-8", errors="replace")
            opens = content.count("{{")
            closes = content.count("}}")
            if opens != closes:
                unbalanced.append(f"{path.relative_to(PROJECT_ROOT)}: {{ {opens} vs }} {closes}")
        assert not unbalanced, "Unbalanced Jinja2 expressions:\n" + "\n".join(unbalanced)

    def test_template_count_minimum(self):
        """At least 40 templates exist (catches accidental mass deletion)."""
        all_files = _get_all_template_files()
        assert len(all_files) >= 40, f"Expected >=40 templates, found {len(all_files)}"

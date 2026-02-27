"""Error recovery tests — verify JVIS fails clearly on broken inputs.

Tests use tmp_path fixtures with deliberately broken inputs to verify
graceful error handling, clear logging, and no silent failures.
"""

from __future__ import annotations

import logging
import os
from pathlib import Path

import pytest
import yaml
from jinja2.exceptions import TemplateSyntaxError

from jvis.scaffold.stack_runner import _build_context, _process_file
from jvis.stacks.registry import _load_manifest, discover_stacks
from jvis.utils.fs import copy_tree, is_empty_dir, is_writable, write_file
from jvis.utils.validation import (
    sanitize_project_name,
    validate_project_name,
    validate_safe_path,
)

# ---------------------------------------------------------------------------
# Broken Jinja2 templates
# ---------------------------------------------------------------------------


class TestBrokenTemplates:
    """Tests for broken Jinja2 template handling."""

    def test_invalid_jinja2_syntax_raises_clear_error(self, tmp_path):
        """A .j2 file with syntax error raises TemplateSyntaxError."""
        files_dir = tmp_path / "files"
        files_dir.mkdir()
        broken = files_dir / "broken.py.j2"
        broken.write_text("{% if True %}\nmissing endif\n")

        ctx = _build_context("test-proj", "desc", "postgresql")
        entry = {"src": "broken.py.j2", "dst": "broken.py.j2"}

        with pytest.raises(TemplateSyntaxError):
            _process_file(entry, files_dir, tmp_path / "out", ctx)

    def test_undefined_variable_renders_empty(self, tmp_path):
        """Undefined template variables render as empty string (permissive mode)."""
        files_dir = tmp_path / "files"
        files_dir.mkdir()
        out_dir = tmp_path / "out"
        out_dir.mkdir()

        template = files_dir / "config.py.j2"
        template.write_text("name={{ project_name }}\nfoo={{ nonexistent_var }}\n")

        ctx = _build_context("test-proj", "desc", "postgresql")
        entry = {"src": "config.py.j2", "dst": "config.py.j2"}

        _process_file(entry, files_dir, out_dir, ctx)

        output = (out_dir / "config.py").read_text()
        assert "name=test-proj" in output
        assert "foo=" in output

    def test_missing_template_file_logs_warning(self, tmp_path, caplog):
        """Manifest referencing non-existent template logs warning and skips."""
        files_dir = tmp_path / "files"
        files_dir.mkdir()

        ctx = _build_context("test-proj", "desc", "postgresql")
        entry = {"src": "does_not_exist.py.j2", "dst": "output.py"}

        with caplog.at_level(logging.WARNING, logger="jvis.scaffold.stack_runner"):
            _process_file(entry, files_dir, tmp_path / "out", ctx)

        assert "not found" in caplog.text.lower()
        assert not (tmp_path / "out" / "output.py").exists()

    def test_template_renders_all_context_vars(self, tmp_path):
        """All standard context variables are available in templates."""
        files_dir = tmp_path / "files"
        files_dir.mkdir()
        out_dir = tmp_path / "out"
        out_dir.mkdir()

        template = files_dir / "check.txt.j2"
        template.write_text(
            "name={{ project_name }}\ndesc={{ project_description }}\ndb={{ database_type }}\ndate={{ date }}\n"
        )

        ctx = _build_context("myapp", "My App", "mysql")
        _process_file({"src": "check.txt.j2", "dst": "check.txt.j2"}, files_dir, out_dir, ctx)

        output = (out_dir / "check.txt").read_text()
        assert "name=myapp" in output
        assert "desc=My App" in output
        assert "db=mysql" in output
        assert "date=" in output


# ---------------------------------------------------------------------------
# Malformed manifests
# ---------------------------------------------------------------------------


class TestMalformedManifests:
    """Tests for malformed YAML manifest handling."""

    def test_malformed_yaml_raises_yaml_error(self, tmp_path):
        """Malformed YAML in manifest.yaml raises yaml.YAMLError."""
        stack_dir = tmp_path / "broken-stack"
        stack_dir.mkdir()
        manifest = stack_dir / "manifest.yaml"
        manifest.write_text("id: broken\nname: [\ninvalid yaml\n")

        with pytest.raises(yaml.YAMLError):
            _load_manifest(manifest)

    def test_manifest_missing_required_field_raises_key_error(self, tmp_path):
        """A manifest missing 'id' or 'name' raises KeyError."""
        stack_dir = tmp_path / "broken-stack"
        stack_dir.mkdir()
        manifest = stack_dir / "manifest.yaml"
        manifest.write_text("description: missing id and name\ntype: backend\n")

        with pytest.raises(KeyError):
            _load_manifest(manifest)

    def test_empty_dev_command_uses_default(self, tmp_path):
        """A manifest with no dev_command gets empty string default."""
        stack_dir = tmp_path / "test-stack"
        stack_dir.mkdir()
        manifest = stack_dir / "manifest.yaml"
        manifest.write_text(yaml.dump({"id": "test", "name": "Test Stack", "type": "backend"}))

        info = _load_manifest(manifest)
        assert info.dev_command == ""
        assert info.dev_port == 8000

    def test_empty_getting_started_uses_default(self, tmp_path):
        """A manifest with no getting_started gets empty dict default."""
        stack_dir = tmp_path / "test-stack"
        stack_dir.mkdir()
        manifest = stack_dir / "manifest.yaml"
        manifest.write_text(yaml.dump({"id": "test", "name": "Test Stack", "type": "backend"}))

        info = _load_manifest(manifest)
        assert info.getting_started == {}

    def test_discover_stacks_skips_broken_manifest(self, tmp_path, caplog, monkeypatch):
        """discover_stacks() skips broken manifests and continues with valid ones."""
        stacks_dir = tmp_path / "stacks"

        good = stacks_dir / "good-stack"
        good.mkdir(parents=True)
        (good / "manifest.yaml").write_text(
            yaml.dump(
                {
                    "id": "good",
                    "name": "Good Stack",
                    "type": "backend",
                    "language": "python",
                    "framework": "flask",
                }
            )
        )

        broken = stacks_dir / "broken-stack"
        broken.mkdir(parents=True)
        (broken / "manifest.yaml").write_text("id: [broken\n")

        monkeypatch.setattr("jvis.stacks.registry._get_stacks_dir", lambda: stacks_dir)
        discover_stacks.cache_clear()

        with caplog.at_level(logging.WARNING, logger="jvis.stacks.registry"):
            stacks = discover_stacks()

        discover_stacks.cache_clear()  # clean up for other tests

        assert "good" in stacks
        assert "broken" not in stacks
        assert "skipping" in caplog.text.lower()


# ---------------------------------------------------------------------------
# Permission errors
# ---------------------------------------------------------------------------


class TestPermissionErrors:
    """Tests for permission-denied scenarios."""

    @pytest.mark.skipif(os.name == "nt", reason="chmod not reliable on Windows")
    def test_readonly_output_dir_raises_permission_error(self, tmp_path):
        """Writing to a read-only directory raises PermissionError."""
        if hasattr(os, "getuid") and os.getuid() == 0:
            pytest.skip("Cannot test permissions as root")

        readonly_dir = tmp_path / "readonly"
        readonly_dir.mkdir()
        os.chmod(readonly_dir, 0o555)

        try:
            with pytest.raises(PermissionError):
                write_file(readonly_dir / "test.txt", "content")
        finally:
            os.chmod(readonly_dir, 0o755)

    @pytest.mark.skipif(os.name == "nt", reason="chmod not reliable on Windows")
    def test_no_partial_files_on_permission_error(self, tmp_path):
        """No partial output files when a permission error occurs."""
        if hasattr(os, "getuid") and os.getuid() == 0:
            pytest.skip("Cannot test permissions as root")

        readonly_dir = tmp_path / "readonly"
        readonly_dir.mkdir()
        os.chmod(readonly_dir, 0o555)

        try:
            with pytest.raises(PermissionError):
                write_file(readonly_dir / "should_not_exist.txt", "content")
            assert not (readonly_dir / "should_not_exist.txt").exists()
        finally:
            os.chmod(readonly_dir, 0o755)

    @pytest.mark.skipif(os.name == "nt", reason="chmod not reliable on Windows")
    def test_is_writable_on_readonly_dir(self, tmp_path):
        """is_writable returns False for read-only directory."""
        if hasattr(os, "getuid") and os.getuid() == 0:
            pytest.skip("Cannot test permissions as root")

        readonly = tmp_path / "readonly"
        readonly.mkdir()
        os.chmod(readonly, 0o444)

        try:
            assert not is_writable(readonly)
        finally:
            os.chmod(readonly, 0o755)


# ---------------------------------------------------------------------------
# Input validation / security
# ---------------------------------------------------------------------------


class TestInputValidation:
    """Tests for input validation edge cases and injection prevention."""

    def test_project_name_with_jinja2_curly_braces_rejected(self):
        """Project name containing {{ is rejected by validation."""
        result = validate_project_name("{{malicious}}")
        assert result is not None
        assert "must start with a letter" in result

    def test_project_name_with_jinja2_block_syntax_rejected(self):
        """Project name containing {% is rejected by validation."""
        result = validate_project_name("{%import os%}")
        assert result is not None

    def test_project_name_with_shell_injection_rejected(self):
        """Project name with shell metacharacters is rejected."""
        for bad_name in ("test;rm", "test$(pwd)", "test`id`", "test|cat"):
            result = validate_project_name(bad_name)
            assert result is not None, f"Should reject: {bad_name}"

    def test_sanitize_strips_jinja2_syntax(self):
        """sanitize_project_name strips Jinja2 injection characters."""
        result = sanitize_project_name("{{my-project}}")
        assert "{{" not in result
        assert "{%" not in result

    def test_empty_project_name_rejected(self):
        """Empty project name returns clear error."""
        result = validate_project_name("")
        assert result is not None
        assert "empty" in result.lower()

    def test_too_long_project_name_rejected(self):
        """Project name exceeding 64 chars is rejected."""
        result = validate_project_name("a" * 65)
        assert result is not None

    def test_traversal_path_rejected(self):
        """Path with .. traversal is rejected."""
        result = validate_safe_path(Path("../../../etc/passwd"))
        assert result is not None
        assert "traversal" in result.lower()

    def test_system_path_rejected(self):
        """System directory paths are rejected."""
        for path in ("/", "/etc", "/var", "/usr"):
            result = validate_safe_path(Path(path))
            assert result is not None, f"Should reject: {path}"


# ---------------------------------------------------------------------------
# Filesystem edge cases
# ---------------------------------------------------------------------------


class TestFileSystemEdgeCases:
    """Tests for filesystem utility edge cases."""

    def test_is_empty_dir_on_nonexistent_path(self, tmp_path):
        """is_empty_dir returns False for non-existent path."""
        assert not is_empty_dir(tmp_path / "nonexistent")

    def test_is_empty_dir_on_file(self, tmp_path):
        """is_empty_dir returns False when given a file path."""
        file = tmp_path / "file.txt"
        file.write_text("content")
        assert not is_empty_dir(file)

    def test_copy_tree_skips_nonexistent_source(self, tmp_path):
        """copy_tree silently skips non-existent source directory."""
        dst = tmp_path / "dst"
        copy_tree(tmp_path / "nonexistent", dst)
        assert not dst.exists()

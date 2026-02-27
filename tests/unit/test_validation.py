"""Tests for jvis.utils.validation."""

from __future__ import annotations

from pathlib import Path

from jvis.utils.validation import sanitize_project_name, validate_description, validate_project_name, validate_safe_path


class TestSanitizeProjectName:
    def test_lowercase(self):
        assert sanitize_project_name("MyProject") == "myproject"

    def test_spaces_to_hyphens(self):
        assert sanitize_project_name("my project") == "my-project"

    def test_dots_to_hyphens(self):
        assert sanitize_project_name("my.project") == "my-project"

    def test_strip_special_chars(self):
        assert sanitize_project_name("my@project!") == "myproject"

    def test_strip_leading_hyphens(self):
        assert sanitize_project_name("--my-project--") == "my-project"

    def test_empty_input(self):
        assert sanitize_project_name("   ") == ""

    def test_already_valid(self):
        assert sanitize_project_name("my-project-42") == "my-project-42"


class TestValidateProjectName:
    def test_valid_names(self):
        assert validate_project_name("my-project") is None
        assert validate_project_name("app") is None
        assert validate_project_name("my_project_v2") is None
        assert validate_project_name("ab") is None

    def test_empty(self):
        assert validate_project_name("") is not None

    def test_too_short(self):
        assert validate_project_name("a") is not None

    def test_starts_with_number(self):
        assert validate_project_name("2fast") is not None

    def test_starts_with_hyphen(self):
        assert validate_project_name("-project") is not None

    def test_uppercase(self):
        assert validate_project_name("MyProject") is not None

    def test_spaces(self):
        assert validate_project_name("my project") is not None


class TestValidateSafePath:
    def test_valid_path(self, tmp_path):
        assert validate_safe_path(tmp_path / "my-project") is None

    def test_root_path(self):
        assert validate_safe_path(Path("/")) is not None

    def test_system_dirs(self):
        assert validate_safe_path(Path("/usr")) is not None
        assert validate_safe_path(Path("/etc")) is not None
        assert validate_safe_path(Path("/bin")) is not None

    def test_traversal(self):
        assert validate_safe_path(Path("/home/../etc")) is not None


class TestValidateDescription:
    def test_empty_description_valid(self):
        assert validate_description("") is None

    def test_short_description_valid(self):
        assert validate_description("A simple project") is None

    def test_max_length_valid(self):
        assert validate_description("x" * 512) is None

    def test_over_max_length_invalid(self):
        result = validate_description("x" * 513)
        assert result is not None
        assert "513" in result
        assert "512" in result

    def test_way_over_max_length(self):
        assert validate_description("a" * 10000) is not None

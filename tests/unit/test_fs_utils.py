"""Tests for jvis.utils.fs — filesystem helpers."""

from __future__ import annotations

import stat
from pathlib import Path

from jvis.utils.fs import copy_file, copy_tree, is_empty_dir, is_writable, mkdir_p, write_file

# =============================================================================
# mkdir_p
# =============================================================================


class TestMkdirP:
    def test_creates_nested_dirs(self, tmp_path: Path) -> None:
        target = tmp_path / "a" / "b" / "c"
        mkdir_p(target)
        assert target.is_dir()

    def test_no_error_if_exists(self, tmp_path: Path) -> None:
        target = tmp_path / "existing"
        target.mkdir()
        mkdir_p(target)  # should not raise
        assert target.is_dir()


# =============================================================================
# write_file
# =============================================================================


class TestWriteFile:
    def test_writes_content(self, tmp_path: Path) -> None:
        target = tmp_path / "hello.txt"
        write_file(target, "hello world")
        assert target.read_text() == "hello world"

    def test_creates_parent_dirs(self, tmp_path: Path) -> None:
        target = tmp_path / "deep" / "nested" / "file.txt"
        write_file(target, "content")
        assert target.read_text() == "content"

    def test_overwrites_existing(self, tmp_path: Path) -> None:
        target = tmp_path / "file.txt"
        write_file(target, "first")
        write_file(target, "second")
        assert target.read_text() == "second"


# =============================================================================
# copy_tree
# =============================================================================


class TestCopyTree:
    def test_copies_directory(self, tmp_path: Path) -> None:
        src = tmp_path / "src"
        src.mkdir()
        (src / "a.txt").write_text("a")
        (src / "sub").mkdir()
        (src / "sub" / "b.txt").write_text("b")

        dst = tmp_path / "dst"
        copy_tree(src, dst)
        assert (dst / "a.txt").read_text() == "a"
        assert (dst / "sub" / "b.txt").read_text() == "b"

    def test_noop_for_nonexistent_src(self, tmp_path: Path) -> None:
        dst = tmp_path / "dst"
        copy_tree(tmp_path / "nonexistent", dst)
        assert not dst.exists()

    def test_merges_into_existing(self, tmp_path: Path) -> None:
        src = tmp_path / "src"
        src.mkdir()
        (src / "new.txt").write_text("new")

        dst = tmp_path / "dst"
        dst.mkdir()
        (dst / "existing.txt").write_text("existing")

        copy_tree(src, dst)
        assert (dst / "existing.txt").read_text() == "existing"
        assert (dst / "new.txt").read_text() == "new"


# =============================================================================
# copy_file
# =============================================================================


class TestCopyFile:
    def test_copies_single_file(self, tmp_path: Path) -> None:
        src = tmp_path / "src.txt"
        src.write_text("content")
        dst = tmp_path / "dst.txt"
        copy_file(src, dst)
        assert dst.read_text() == "content"

    def test_creates_destination_dir(self, tmp_path: Path) -> None:
        src = tmp_path / "src.txt"
        src.write_text("content")
        dst = tmp_path / "deep" / "nested" / "dst.txt"
        copy_file(src, dst)
        assert dst.read_text() == "content"


# =============================================================================
# is_empty_dir
# =============================================================================


class TestIsEmptyDir:
    def test_true_for_empty_dir(self, tmp_path: Path) -> None:
        empty = tmp_path / "empty"
        empty.mkdir()
        assert is_empty_dir(empty) is True

    def test_false_for_non_empty(self, tmp_path: Path) -> None:
        (tmp_path / "file.txt").write_text("x")
        assert is_empty_dir(tmp_path) is False

    def test_false_for_nonexistent(self, tmp_path: Path) -> None:
        assert is_empty_dir(tmp_path / "nope") is False

    def test_false_for_file(self, tmp_path: Path) -> None:
        f = tmp_path / "file.txt"
        f.write_text("x")
        assert is_empty_dir(f) is False


# =============================================================================
# is_writable
# =============================================================================


class TestIsWritable:
    def test_writable_dir(self, tmp_path: Path) -> None:
        assert is_writable(tmp_path) is True

    def test_writable_file(self, tmp_path: Path) -> None:
        f = tmp_path / "file.txt"
        f.write_text("x")
        assert is_writable(f) is True

    def test_readonly_file(self, tmp_path: Path) -> None:
        f = tmp_path / "readonly.txt"
        f.write_text("x")
        f.chmod(stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)
        try:
            assert is_writable(f) is False
        finally:
            # Restore write permission so tmp_path cleanup works
            f.chmod(stat.S_IRUSR | stat.S_IWUSR)

    def test_nonexistent_path(self, tmp_path: Path) -> None:
        assert is_writable(tmp_path / "nope") is False

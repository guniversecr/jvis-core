"""Tests for jvis.scaffold.entity_rename — post-processing entity name replacement."""

from __future__ import annotations

from pathlib import Path

from jvis.scaffold.entity_rename import apply_entity_name


class TestApplyEntityName:
    """Unit tests for apply_entity_name()."""

    def test_noop_when_default_item(self, tmp_path: Path):
        f = tmp_path / "item.py"
        f.write_text("class ItemService: pass")
        apply_entity_name(tmp_path, "item")
        assert f.read_text() == "class ItemService: pass"
        assert f.name == "item.py"

    def test_replaces_file_content(self, tmp_path: Path):
        f = tmp_path / "service.py"
        f.write_text("class ItemService:\n    items = []\n    ITEM_COUNT = 0\n")
        apply_entity_name(tmp_path, "product")
        result = f.read_text()
        assert "ProductService" in result
        assert "products" in result
        assert "PRODUCT_COUNT" in result
        assert "Item" not in result

    def test_renames_files(self, tmp_path: Path):
        f = tmp_path / "item.py"
        f.write_text("# item module")
        apply_entity_name(tmp_path, "product")
        assert not (tmp_path / "item.py").exists()
        renamed = tmp_path / "product.py"
        assert renamed.exists()
        assert "product module" in renamed.read_text()

    def test_renames_directories(self, tmp_path: Path):
        d = tmp_path / "items"
        d.mkdir()
        (d / "readme.txt").write_text("items list")
        apply_entity_name(tmp_path, "product")
        assert not (tmp_path / "items").exists()
        assert (tmp_path / "products").is_dir()
        assert "products list" in (tmp_path / "products" / "readme.txt").read_text()

    def test_preserves_non_entity_content(self, tmp_path: Path):
        f = tmp_path / "config.py"
        f.write_text("DATABASE_URL = 'postgres://localhost'\nDEBUG = True\n")
        apply_entity_name(tmp_path, "product")
        result = f.read_text()
        assert "DATABASE_URL = 'postgres://localhost'" in result
        assert "DEBUG = True" in result

    def test_handles_all_case_variants(self, tmp_path: Path):
        f = tmp_path / "mixed.py"
        f.write_text("Item items ITEMS item_service Items ITEM\n")
        apply_entity_name(tmp_path, "task")
        result = f.read_text()
        assert "Task" in result
        assert "tasks" in result
        assert "TASKS" in result
        assert "task_service" in result
        assert "Tasks" in result
        assert "TASK" in result
        assert "Item" not in result
        assert "item" not in result

    def test_angular_template_preserved(self, tmp_path: Path):
        f = tmp_path / "component.html"
        f.write_text('<div>{{ item.name }}</div>\n<li *ngFor="let item of items">')
        apply_entity_name(tmp_path, "product")
        result = f.read_text()
        assert "{{ product.name }}" in result
        assert "let product of products" in result

    def test_skips_binary_extensions(self, tmp_path: Path):
        f = tmp_path / "cache.pyc"
        f.write_bytes(b"\x00\x01Item\x02\x03")
        apply_entity_name(tmp_path, "product")
        assert f.read_bytes() == b"\x00\x01Item\x02\x03"

    def test_skips_git_directory(self, tmp_path: Path):
        git_dir = tmp_path / ".git"
        git_dir.mkdir()
        f = git_dir / "config"
        f.write_text("item")
        apply_entity_name(tmp_path, "product")
        assert f.read_text() == "item"

    def test_nested_file_and_dir_rename(self, tmp_path: Path):
        d = tmp_path / "src" / "items"
        d.mkdir(parents=True)
        f = d / "item_model.py"
        f.write_text("class Item:\n    pass\n")
        apply_entity_name(tmp_path, "order")
        renamed_dir = tmp_path / "src" / "orders"
        assert renamed_dir.is_dir()
        renamed_file = renamed_dir / "order_model.py"
        assert renamed_file.exists()
        assert "class Order:" in renamed_file.read_text()

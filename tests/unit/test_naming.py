"""Tests for jvis.utils.naming — pluralization and entity replacement pairs."""

from __future__ import annotations

from jvis.utils.naming import entity_replacements, pluralize


class TestPluralize:
    """Unit tests for naive English pluralization."""

    def test_regular(self):
        assert pluralize("product") == "products"

    def test_es_suffix_s(self):
        assert pluralize("address") == "addresses"

    def test_es_suffix_x(self):
        assert pluralize("box") == "boxes"

    def test_es_suffix_ch(self):
        assert pluralize("match") == "matches"

    def test_es_suffix_sh(self):
        assert pluralize("dish") == "dishes"

    def test_es_suffix_z(self):
        # Naive pluralizer doesn't double the z (quiz→quizes, not quizzes).
        # Good enough for common entity names (buzz→buzzes works via -ss path).
        assert pluralize("quiz") == "quizes"

    def test_y_suffix_consonant(self):
        assert pluralize("category") == "categories"

    def test_y_suffix_vowel(self):
        assert pluralize("key") == "keys"

    def test_already_plural(self):
        assert pluralize("items") == "items"

    def test_empty(self):
        assert pluralize("") == ""

    def test_single_char(self):
        assert pluralize("a") == "as"

    def test_common_entities(self):
        assert pluralize("user") == "users"
        assert pluralize("task") == "tasks"
        assert pluralize("article") == "articles"
        assert pluralize("order") == "orders"


class TestEntityReplacements:
    """Unit tests for entity_replacements() pair generation."""

    def test_identity_returns_empty(self):
        assert entity_replacements("item", "item") == []

    def test_returns_six_pairs(self):
        pairs = entity_replacements("item", "product")
        assert len(pairs) == 6

    def test_correct_order(self):
        pairs = entity_replacements("item", "product")
        old_values = [old for old, _ in pairs]
        assert old_values == ["ITEMS", "Items", "items", "ITEM", "Item", "item"]

    def test_new_values(self):
        pairs = entity_replacements("item", "product")
        new_values = [new for _, new in pairs]
        assert new_values == ["PRODUCTS", "Products", "products", "PRODUCT", "Product", "product"]

    def test_y_suffix_entity(self):
        pairs = entity_replacements("item", "category")
        new_values = [new for _, new in pairs]
        assert "Categories" in new_values
        assert "categories" in new_values
        assert "Category" in new_values

    def test_case_preservation(self):
        pairs = entity_replacements("item", "task")
        pairs_dict = dict(pairs)
        assert pairs_dict["Item"] == "Task"
        assert pairs_dict["item"] == "task"
        assert pairs_dict["ITEM"] == "TASK"
        assert pairs_dict["Items"] == "Tasks"
        assert pairs_dict["items"] == "tasks"
        assert pairs_dict["ITEMS"] == "TASKS"

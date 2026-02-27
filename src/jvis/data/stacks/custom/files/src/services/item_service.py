"""Item service — in-memory CRUD operations."""

from __future__ import annotations

from datetime import datetime, timezone

from src.models import Item

# In-memory storage
_items: dict[str, Item] = {}


class ItemService:
    """Service layer for Item CRUD operations."""

    @staticmethod
    def create(name: str, description: str = "") -> Item:
        item = Item(name=name, description=description)
        _items[item.id] = item
        return item

    @staticmethod
    def get_all() -> list[Item]:
        return sorted(_items.values(), key=lambda i: i.created_at, reverse=True)

    @staticmethod
    def get_by_id(item_id: str) -> Item | None:
        return _items.get(item_id)

    @staticmethod
    def update(item: Item, name: str | None = None, description: str | None = None) -> Item:
        if name is not None:
            item.name = name
        if description is not None:
            item.description = description
        item.updated_at = datetime.now(timezone.utc).isoformat()
        return item

    @staticmethod
    def delete(item_id: str) -> bool:
        return _items.pop(item_id, None) is not None

    @staticmethod
    def clear() -> None:
        _items.clear()

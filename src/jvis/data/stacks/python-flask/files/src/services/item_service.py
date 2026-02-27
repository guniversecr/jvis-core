"""Item business logic."""

from src.app import db
from src.models import Item


class ItemService:
    """Service layer for Item CRUD operations."""

    @staticmethod
    def create(name: str, description: str = "") -> Item:
        item = Item(name=name, description=description)
        db.session.add(item)
        db.session.commit()
        return item

    @staticmethod
    def get_all() -> list[Item]:
        return Item.query.order_by(Item.created_at.desc()).all()

    @staticmethod
    def get_by_id(item_id: str) -> Item | None:
        return db.session.get(Item, item_id)

    @staticmethod
    def update(item: Item, name: str | None = None, description: str | None = None) -> Item:
        if name is not None:
            item.name = name
        if description is not None:
            item.description = description
        db.session.commit()
        return item

    @staticmethod
    def delete(item: Item) -> None:
        db.session.delete(item)
        db.session.commit()

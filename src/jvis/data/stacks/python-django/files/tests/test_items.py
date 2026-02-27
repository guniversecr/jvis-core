"""Item CRUD tests for Django REST Framework."""

import pytest
from core.models import Item
from django.test import Client


@pytest.fixture
def client() -> Client:
    return Client()


@pytest.mark.django_db
class TestItemCRUD:
    """Test Item CRUD operations via DRF ViewSet."""

    def test_create_item(self, client: Client) -> None:
        response = client.post(
            "/api/items/",
            data={"name": "Test Item", "description": "A test item"},
            content_type="application/json",
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Test Item"
        assert data["description"] == "A test item"
        assert "id" in data
        assert "created_at" in data

    def test_list_items(self, client: Client) -> None:
        Item.objects.create(name="Item 1", description="First")
        Item.objects.create(name="Item 2", description="Second")

        response = client.get("/api/items/")
        assert response.status_code == 200
        data = response.json()
        assert data["count"] == 2

    def test_get_item(self, client: Client) -> None:
        item = Item.objects.create(name="Test", description="Desc")

        response = client.get(f"/api/items/{item.id}/")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Test"

    def test_update_item(self, client: Client) -> None:
        item = Item.objects.create(name="Old Name")

        response = client.patch(
            f"/api/items/{item.id}/",
            data={"name": "New Name"},
            content_type="application/json",
        )
        assert response.status_code == 200
        assert response.json()["name"] == "New Name"

    def test_delete_item(self, client: Client) -> None:
        item = Item.objects.create(name="To Delete")

        response = client.delete(f"/api/items/{item.id}/")
        assert response.status_code == 204
        assert Item.objects.count() == 0

    def test_get_nonexistent_returns_404(self, client: Client) -> None:
        response = client.get("/api/items/00000000-0000-0000-0000-000000000000/")
        assert response.status_code == 404

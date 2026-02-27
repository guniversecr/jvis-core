"""Tests for Item CRUD — unit (service) + integration (HTTP)."""

from __future__ import annotations

import json
import threading
import urllib.error
import urllib.request
from http.server import HTTPServer
from unittest import TestCase

from src.handlers import ItemHandler
from src.services.item_service import ItemService


class TestItemService(TestCase):
    """Unit tests for ItemService."""

    def setUp(self) -> None:
        ItemService.clear()

    def test_create_item(self) -> None:
        item = ItemService.create("Test Item", "A description")
        assert item.name == "Test Item"
        assert item.description == "A description"
        assert item.id is not None

    def test_list_items(self) -> None:
        ItemService.create("Item 1")
        ItemService.create("Item 2")
        items = ItemService.get_all()
        assert len(items) == 2

    def test_get_by_id(self) -> None:
        item = ItemService.create("Find Me")
        found = ItemService.get_by_id(item.id)
        assert found is not None
        assert found.name == "Find Me"

    def test_get_by_id_not_found(self) -> None:
        assert ItemService.get_by_id("nonexistent") is None

    def test_update_item(self) -> None:
        item = ItemService.create("Old Name")
        ItemService.update(item, name="New Name")
        assert item.name == "New Name"

    def test_delete_item(self) -> None:
        item = ItemService.create("Delete Me")
        assert ItemService.delete(item.id) is True
        assert ItemService.get_by_id(item.id) is None

    def test_delete_not_found(self) -> None:
        assert ItemService.delete("nonexistent") is False


class TestItemHTTP(TestCase):
    """Integration tests for HTTP endpoints."""

    server: HTTPServer
    thread: threading.Thread
    base_url: str

    @classmethod
    def setUpClass(cls) -> None:
        cls.server = HTTPServer(("127.0.0.1", 0), ItemHandler)
        port = cls.server.server_address[1]
        cls.base_url = f"http://127.0.0.1:{port}"
        cls.thread = threading.Thread(target=cls.server.serve_forever)
        cls.thread.daemon = True
        cls.thread.start()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.server.shutdown()

    def setUp(self) -> None:
        ItemService.clear()

    def _request(self, method: str, path: str, body: dict | None = None) -> tuple[int, dict | list]:
        data = json.dumps(body).encode("utf-8") if body else None
        req = urllib.request.Request(
            f"{self.base_url}{path}",
            data=data,
            method=method,
            headers={"Content-Type": "application/json"} if data else {},
        )
        try:
            with urllib.request.urlopen(req) as resp:
                content = resp.read().decode("utf-8")
                return resp.status, json.loads(content) if content else {}
        except urllib.error.HTTPError as e:
            content = e.read().decode("utf-8")
            return e.code, json.loads(content) if content else {}

    def test_health_check(self) -> None:
        status, data = self._request("GET", "/api/health")
        assert status == 200
        assert data["status"] == "ok"

    def test_create_item_http(self) -> None:
        status, data = self._request("POST", "/api/items", {"name": "HTTP Item"})
        assert status == 201
        assert data["name"] == "HTTP Item"

    def test_list_items_http(self) -> None:
        self._request("POST", "/api/items", {"name": "Item 1"})
        self._request("POST", "/api/items", {"name": "Item 2"})
        status, data = self._request("GET", "/api/items")
        assert status == 200
        assert len(data) == 2

    def test_get_item_http(self) -> None:
        _, created = self._request("POST", "/api/items", {"name": "Get Me"})
        status, data = self._request("GET", f"/api/items/{created['id']}")
        assert status == 200
        assert data["name"] == "Get Me"

    def test_update_item_http(self) -> None:
        _, created = self._request("POST", "/api/items", {"name": "Old"})
        status, data = self._request("PATCH", f"/api/items/{created['id']}", {"name": "New"})
        assert status == 200
        assert data["name"] == "New"

    def test_delete_item_http(self) -> None:
        _, created = self._request("POST", "/api/items", {"name": "Gone"})
        req = urllib.request.Request(
            f"{self.base_url}/api/items/{created['id']}",
            method="DELETE",
        )
        with urllib.request.urlopen(req) as resp:
            assert resp.status == 204

    def test_create_item_missing_name(self) -> None:
        status, data = self._request("POST", "/api/items", {"description": "no name"})
        assert status == 400

    def test_get_item_not_found(self) -> None:
        status, _ = self._request("GET", "/api/items/nonexistent")
        assert status == 404

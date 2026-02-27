"""HTTP request handler — CRUD routes via regex, pure stdlib."""

from __future__ import annotations

import json
import re
from http.server import BaseHTTPRequestHandler

from src.services.item_service import ItemService

ITEMS_LIST = re.compile(r"^/api/items/?$")
ITEMS_DETAIL = re.compile(r"^/api/items/([^/]+)/?$")
HEALTH = re.compile(r"^/api/health/?$")


class ItemHandler(BaseHTTPRequestHandler):
    """HTTP handler for Item CRUD endpoints."""

    def do_GET(self) -> None:
        if HEALTH.match(self.path):
            self._json_response(200, {"status": "ok"})
        elif ITEMS_LIST.match(self.path):
            items = [item.to_dict() for item in ItemService.get_all()]
            self._json_response(200, items)
        elif m := ITEMS_DETAIL.match(self.path):
            item = ItemService.get_by_id(m.group(1))
            if item:
                self._json_response(200, item.to_dict())
            else:
                self._json_response(404, {"error": "Item not found"})
        else:
            self._json_response(404, {"error": "Not found"})

    def do_POST(self) -> None:
        if ITEMS_LIST.match(self.path):
            body = self._read_body()
            if not body or "name" not in body:
                self._json_response(400, {"error": "name is required"})
                return
            item = ItemService.create(body["name"], body.get("description", ""))
            self._json_response(201, item.to_dict())
        else:
            self._json_response(404, {"error": "Not found"})

    def do_PATCH(self) -> None:
        if m := ITEMS_DETAIL.match(self.path):
            item = ItemService.get_by_id(m.group(1))
            if not item:
                self._json_response(404, {"error": "Item not found"})
                return
            body = self._read_body()
            ItemService.update(item, body.get("name"), body.get("description"))
            self._json_response(200, item.to_dict())
        else:
            self._json_response(404, {"error": "Not found"})

    def do_DELETE(self) -> None:
        if m := ITEMS_DETAIL.match(self.path):
            if ItemService.delete(m.group(1)):
                self._send_status(204)
            else:
                self._json_response(404, {"error": "Item not found"})
        else:
            self._json_response(404, {"error": "Not found"})

    def _read_body(self) -> dict:
        length = int(self.headers.get("Content-Length", 0))
        if length == 0:
            return {}
        raw = self.rfile.read(length)
        return json.loads(raw)

    def _json_response(self, status: int, data: dict | list) -> None:
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_status(self, status: int) -> None:
        self.send_response(status)
        self.end_headers()

    def log_message(self, format: str, *args: object) -> None:  # noqa: A002
        pass  # Silence request logs during tests

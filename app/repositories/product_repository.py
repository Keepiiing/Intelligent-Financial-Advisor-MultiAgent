import json
from pathlib import Path


class ProductRepository:
    def __init__(self, data_path: Path) -> None:
        self.data_path = data_path
        self._products = self._load_products()

    def _load_products(self) -> list[dict]:
        return json.loads(self.data_path.read_text(encoding="utf-8"))

    def list_products(self) -> list[dict]:
        return self._products

    def get_by_id(self, product_id: str) -> dict | None:
        return next((item for item in self._products if item["id"] == product_id), None)

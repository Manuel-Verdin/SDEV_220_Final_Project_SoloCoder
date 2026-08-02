import json
from pathlib import Path
from models import RepairShop

class DataStorage:
    def __init__(self, file_path="repair_shop_data.json"):
        self.file_path = Path(file_path)

    def save(self, shop: RepairShop) -> None:
        self.file_path.write_text(json.dumps(shop.to_dict(), indent=4), encoding="utf-8")

    def load(self) -> RepairShop:
        if not self.file_path.exists():
            return RepairShop()
        try:
            return RepairShop.from_dict(json.loads(self.file_path.read_text(encoding="utf-8")))
        except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
            raise ValueError(f"Unable to load saved data: {error}") from error

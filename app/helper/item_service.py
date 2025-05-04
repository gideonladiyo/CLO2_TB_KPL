from app.utils.file_path import file_path
from app.utils.stock_price_validation import validate_item
from app.utils.generate_id import generate_random_id
from app.models import *
import json
from fastapi import HTTPException
from typing import List

class ItemService:
    def __init__(self):
        self.item_path = file_path.ITEMS_PATH
        self.items = self.load_items()

    def load_items(self) -> List:
        try:
            with open(self.item_path, "r") as f:
                data = json.load(f)
                return data
        except (json.JSONDecodeError, FileNotFoundError, ValueError) as e:
            print(f"[Error] Failed to load data: {e}")

    def save_items(self):
        try:
            with open(self.item_path, "w") as f:
                json.dump(self.items, f, indent=4)
        except (PermissionError, TypeError, OSError, json.JSONDecodeError) as e:
            print(f"[Error] Failed to save data: {e}")

    def get_all_items(self) -> List:
        # print(self.items)
        return self.items

    def get_item(self, id: str) -> dict:
        for item in self.items:
            if item["item_id"] == id:
                return item

        raise HTTPException(status_code=404, detail="Item tidak ditemukan")

    def create_item(self, item_create:ItemCreate):
        new_id = generate_random_id(ids=[item["item_id"] for item in self.items], startswith="I", digit_number=5)
        validate_item(item=item_create)
        new_data = {
            "item_id": new_id,
            "name": item_create.name,
            "price": item_create.price,
            "stock": item_create.stock
        }
        self.items.append(new_data)
        self.save_items()
        return new_data

    def find_item_idx(self, item_id: str) -> int:
        for idx, item in enumerate(self.items):
            if item["item_id"] == item_id:
                return idx
        return -1

    def update_item(self, item_id: str, item_updated: ItemCreate):
        validate_item(item=item_updated)
        idx = self.find_item_idx(item_id=item_id)
        if idx == -1:
            raise HTTPException(status_code=404, detail="Item tidak ditemukan")
        self.items[idx]["name"] = item_updated.name
        self.items[idx]["price"] = item_updated.price
        self.items[idx]["stock"] = item_updated.stock
        self.save_items()
        return self.items[idx]

    def delete_item(self, item_id: str):
        idx = self.find_item_idx(item_id=item_id)
        if idx == -1:
            raise HTTPException(status_code=404, detail="Item tidak ditemukan")
        del self.items[idx]
        self.save_items()
        return {"message": f"Item dengan id {item_id} telah dihapus"}

    def buy_item(self, id: str, qty: int):
        current_item = self.get_item(id=id)
        print(current_item)
        if current_item["stock"] < qty:
            raise HTTPException(status_code=400, detail="Stok tidak cukup")
        current_item["stock"] -= qty
        print(current_item)
        self.save_items()

item_service = ItemService()

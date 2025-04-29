from app.utils.file_path import file_path
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
        self.items = self.load_items()
        result = []
        for item in self.items:
            result.append(item)
        return result
    
    def get_item(self, id: str) -> dict:
        self.items = self.load_items()
        for item in self.items:
            if item["item_id"] == id:
                return item
        
        raise HTTPException(status_code=404, detail="Item tidak ditemukan")

    def create_item(self, item_create:ItemCreate):
        new_id = "I00241"
        
        # validasi harga
        if item_create.price > 0:
            new_data = {
                "item_id": new_id,
                "name": item_create.name,
                "price": item_create.price
            }
            self.items.append(new_data)
            self.save_items()
            return new_data
        else:
            raise HTTPException(status_code=400, detail="Harga tidak boleh negatif")
    
    def update_item(self, item_id: str, item_updated: ItemCreate):
        if item_updated.price < 0:
            raise HTTPException(status_code=400, detail="Harga tidak boleh negatif")
        self.items = self.load_items()
        for item in self.items:
            if item["item_id"] == item_id:
                item["name"] = item_updated.name
                item["price"] = item_updated.price
                self.save_items()
                return item
        raise HTTPException(status_code=404, detail="Item tidak ditemukan")

    def delete_item(self, item_id: str):
        self.items = self.load_items()
        for idx, item in enumerate(self.items):
            if item["item_id"] == item_id:
                del self.items[idx]
                self.save_items()
                return {"message": f"Item dengan id {item_id} telah dihapus"}
        raise HTTPException(status_code=404, detail="Item tidak ditemukan")

item_service = ItemService()
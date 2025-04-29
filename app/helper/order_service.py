from helper.file_path import file_path
from fsm.order_fsm import *
from models import *
from typing import List
import json
from datetime import datetime

class OrderService:
    def __init__(self):
        self.order_path = file_path.ORDERS_PATH
        self.orders = self.load_orders()

    def load_orders(self) -> List:
        try:
            with open(self.order_path, "r") as f:
                data = json.load(f)
                return data
        except (json.JSONDecodeError, FileNotFoundError, ValueError) as e:
            print(f"[Error] Failed to load data: {e}")

    def save_orders(self):
        try:
            with open(self.order_path, "w") as f:
                json.dump(self.orders, f, indent=4)
        except (PermissionError, TypeError, OSError, json.JSONDecodeError) as e:
            print(f"[Error] Failed to save data: {e}")

    def get_all_orders(self) -> List:
        self.orders = self.load_orders()
        result = []
        for order in self.orders:
            result.append(order)
        return result

    def get_order(self, id:str) -> dict:
        self.orders = self.load_orders()
        for order in self.orders:
            if order["id"] == id:
                return order

    def create_order(self, order_create: OrderCreate):
        new_id = "O01111"
        current_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")
        new_order = {
            "id": new_id,
            "items": [item.dict() for item in order_create.items],
            "status": "NEW",
            "created_at": current_time,
            "updated_at": current_time
        }
        self.orders.append(new_order)
        self.save_orders()
        
        return new_order
    
    def change_order_state(self, id:str, trigger:str):
        order = self.get_order(id)
        current_state = order["status"]
        new_state = change_order_state(current_state=current_state, trigger=trigger)
        order["status"] = new_state.name
        self.save_orders

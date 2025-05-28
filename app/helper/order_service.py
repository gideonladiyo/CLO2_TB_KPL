from app.utils.file_path import file_path
from app.fsm.order_fsm import change_order_state
from app.models import OrderCreate
from typing import List
import json
from fastapi import HTTPException
from app.helper.item_service import item_service
from app.utils.generate_id import generate_random_id
from app.utils.daily_limit import check_limit_order
from app.utils.current_time import get_current_time_str
from app.config import settings

class OrderService:
    def __init__(self):
        self.order_path = file_path.ORDERS_PATH
        self.orders = self.load_orders()

    def load_orders(self) -> List:
        try:
            with open(self.order_path, "r") as f:
                data = json.load(f)
                return data
        except (FileNotFoundError) as e:
            print(f"[Error] Failed to load data: {e}")

    def save_orders(self):
        try:
            with open(self.order_path, "w") as f:
                json.dump(self.orders, f, indent=4)
        except (FileNotFoundError) as e:
            print(f"[Error] Failed to save data: {e}")

    def get_all_orders(self) -> List:
        return self.orders

    def get_order(self, id:str) -> dict:
        for order in self.orders:
            if order["id"] == id:
                return order
        raise HTTPException(status_code=404)

    def create_order(self, order_create: OrderCreate):
        if len(order_create.items) == 0:
            raise HTTPException(status_code=400, detail="Pesanan tidak boleh kosong")
        orders_date = [order["created_at"] for order in self.orders]
        check_limit_order(orders_date=orders_date, max_order=settings.max_orders_per_day)
        new_id = generate_random_id(ids=[order["id"] for order in self.orders], startswith="O", digit_number=5)
        current_time = get_current_time_str()
        items = []
        for item in order_create.items:
            if item.quantity < 1:
                raise HTTPException(
                    status_code=422, detail="Jumlah barang yang dipesan minimal 1"
                )
            item_service.buy_item(id=item.item_id, qty=item.quantity)
            items.append({
                "item_id": item.item_id,
                "quantity": item.quantity
            })
        new_order = {
            "id": new_id,
            "items": items,
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
        order["updated_at"] = get_current_time_str()
        self.save_orders()

order_service = OrderService()

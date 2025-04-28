from pydantic import BaseModel
from datetime import datetime
from typing import List

class OrderItem(BaseModel):
    item_id: str
    quantity: int

class Order(BaseModel):
    id: str
    items: List[OrderItem]
    status: str
    created_at: datetime
    updated_at: datetime

class OrderItemCreate(BaseModel):
    item_id: str
    quantity: int

class OrderCreate(BaseModel):
    items: List[OrderItemCreate]


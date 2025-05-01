from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional, Generic, TypeVar

class OrderItem(BaseModel):
    item_id: str
    quantity: int

class Order(BaseModel):
    id: str
    items: List[OrderItem]
    status: str
    created_at: datetime
    updated_at: datetime

class OrderStatsResponse(BaseModel):
    NEW: List[Order]
    CANCEL: List[Order]
    PAID: List[Order]
    SHIPPED: List[Order]
    DELIVERED: List[Order]

class OrderItemCreate(BaseModel):
    item_id: str
    quantity: int

class OrderCreate(BaseModel):
    items: List[OrderItemCreate]

class Item(BaseModel):
    item_id: str
    name: str
    price: float
    stock: int

class ItemCreate(BaseModel):
    name: str
    price: float
    stock: int

T = TypeVar('T')

class BaseResponse(BaseModel, Generic[T]):
    status: str
    message: str
    data: Optional[T] = None

from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List, Optional, Generic, TypeVar

class OrderItem(BaseModel):
    item_id: str
    quantity: int

    model_config = ConfigDict(from_attributes=True)

class Order(BaseModel):
    id: str
    items: List[OrderItem]
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class OrderItemCreate(BaseModel):
    item_id: str
    quantity: int

    model_config = ConfigDict(from_attributes=True)

class OrderCreate(BaseModel):
    items: List[OrderItemCreate]

    model_config = ConfigDict(from_attributes=True)

class Item(BaseModel):
    item_id: str
    name: str
    price: float
    stock: int

    model_config = ConfigDict(from_attributes=True)

class ItemCreate(BaseModel):
    name: str
    price: float
    stock: int

    model_config = ConfigDict(from_attributes=True)

T = TypeVar('T')

class BaseResponse(BaseModel, Generic[T]):
    status: str
    message: str
    data: Optional[T] = None

    model_config = ConfigDict(from_attributes=True)

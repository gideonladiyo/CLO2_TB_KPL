from fastapi import APIRouter
from app.helper.order_service import order_service
from typing import List
from app.models import *

router = APIRouter(prefix="/order", tags=["Order"])


@router.get(
    "/",
    response_model=List[Order],
    summary="Daftar pesanan yang ada",
    responses={
        200: {
            "description": "Daftar pesanan berhasil diambil",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": "O51353",
                            "items": [
                                {"item_id": "I23456", "quantity": 2},
                                {"item_id": "I34567", "quantity": 1},
                            ],
                            "status": "NEW",
                            "created_at": "2025-04-28 10:15:00.000000",
                            "updated_at": "2025-04-28 10:15:00.000000",
                        },
                        {
                            "id": "O51354",
                            "items": [{"item_id": "I45678", "quantity": 3}],
                            "status": "PAID",
                            "created_at": "2025-04-28 11:30:22.543210",
                            "updated_at": "2025-04-28 12:05:17.987654",
                        },
                    ]
                }
            },
        }
    },
)
def get_all_items():
    return order_service.get_all_orders()


@router.get(
    "/{id}",
    response_model=Order,
    summary="Daftar pesanan yang ada berdasarkan ID",
    responses={
        200: {
            "description": "Daftar pesanan berhasil diambil",
            "content": {
                "application/json": {
                    "example": {
                        "id": "O51354",
                        "items": [{"item_id": "I45678", "quantity": 3}],
                        "status": "PAID",
                        "created_at": "2025-04-28 11:30:22.543210",
                        "updated_at": "2025-04-28 12:05:17.987654",
                    }
                }
            },
        }
    },
)
def get_all_items(id: str):
    return order_service.get_order(id)


@router.post(
    "/",
    response_model=Order,
    summary="Buat pesanan baru",
    status_code=201,
    responses={
        201: {
            "description": "Pesanan berhasil dibuat",
            "content": {
                "application/json": {
                    "example": {
                        "id": "O12345",
                        "items": [{"item_id": "I45678", "quantity": 3}],
                        "status": "NEW",
                        "created_at": "2025-04-28 13:00:00.000000",
                        "updated_at": "2025-04-28 13:00:00.000000",
                    }
                }
            },
        }
    },
)
def create_order(order_create: OrderCreate):
    return order_service.create_order(order_create)
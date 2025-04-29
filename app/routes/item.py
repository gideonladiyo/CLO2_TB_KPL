from fastapi import APIRouter
from app.helper.item_service import item_service
from typing import List
from app.models import *

router = APIRouter(prefix="/item", tags=["Item"])


@router.get(
    "/",
    response_model=List[Item],
    summary="Daftar barnang yang ada",
    responses={
        200: {
            "description": "Daftar barang berhasil diambil",
            "content": {
                "application/json": {
                    "example": [
                        {"item_id": "I93412", "name": "Laptop", "price": 1000000.00},
                        {"item_id": "I44514", "name": "Keyboard", "price": 350000.00},
                    ]
                }
            },
        }
    },
)
def get_all_items():
    return item_service.get_all_items()


@router.get(
    "/{item_id}",
    response_model=Item,
    summary="Data item berdasarkan id",
    responses={
        200: {
            "description": "Daftar barang berhasil diambil",
            "content": {
                "application/json": {
                    "example": {
                        "item_id": "I44514",
                        "name": "Keyboard",
                        "price": 350000.00,
                    },
                }
            },
        }
    },
)
def get_item_by_id(item_id: str):
    return item_service.get_item(id=item_id)

@router.post(
    "/",
    response_model=Item,
    summary="Menambah item baru",
    status_code=201,
    responses={
        201: {
            "description": "Item berhasil ditambahkan",
            "content": {
                "application/json": {
                    "example": {
                        "item_id": "I44514",
                        "name": "Keyboard",
                        "price": 350000.00,
                    },
                }
            },
        },
        400: {"description": "Harga tidak boleh negatif"},
    },
)
def add_item(item_create: ItemCreate):
    return item_service.create_item(item_create=item_create)

@router.put(
    "/{item_id}",
    response_model=Item,
    summary="Mengubah data item",
    responses = {
        200: {
            "description": "Daftar barang berhasil diupdate",
            "content": {
                "application/json": {
                    "example": {
                        "item_id": "I44514",
                        "name": "Keyboard",
                        "price": 350000.00,
                    },
                }
            },
        }
    },
)
def update_item(item_id: str, item_udpdated: ItemCreate):
    return item_service.update_item(item_id=item_id, item_updated=item_udpdated)

@router.delete(
    "/{item_id}",
    summary="Hapus item berdasarkan item id",
    responses={
        200: {
            "description": "Item berhasil dihapus",
            "content": {
                "application/json": {"example": {"message": "Item berhasil dihapus"}}
            },
        },
        404: {
            "description": "Item tidak ditemukan",
            "content": {
                "application/json": {"example": {"message": "Item tidak ditemukan"}}
            },
        },
    },
)
def delete_item(item_id: str):
    return item_service.delete_item(item_id=item_id)
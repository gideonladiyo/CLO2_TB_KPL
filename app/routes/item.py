from fastapi import APIRouter
from app.helper.item_service import item_service
from typing import List
from app.models import BaseResponse, Item, ItemCreate
from app.commands.item_command import GetItemCommand, GetItemsCommand, CreateItemCommand, UpdateItemCommand, DeleteItemCommand
from app.handlers.command_handler import CommandHandler

router = APIRouter(prefix="/item", tags=["Item"])
handler = CommandHandler()

@router.get(
    "/",
    response_model=BaseResponse[List[Item]],
    summary="Daftar barang yang ada",
    responses={
        200: {
            "description": "Daftar barang berhasil diambil",
            "content": {
                "application/json": {
                    "example": {
                        "status": "Success",
                        "message": "Data barang berhasil diambil",
                        "data": [
                            {
                                "item_id": "I93412",
                                "name": "Laptop",
                                "price": 1000000,
                                "stock": 50,
                            },
                            {
                                "item_id": "I44514",
                                "name": "Keyboard",
                                "price": 350000,
                                "stock": 50,
                            },
                        ],
                    }
                }
            },
        }
    },
)
async def get_all_items():
    command = GetItemsCommand()
    all_item = handler.run(command)
    return BaseResponse(
        status="Success", message="Data barang berhasil diambil", data=all_item
    )


@router.get(
    "/{item_id}",
    response_model=BaseResponse[Item],
    summary="Data item berdasarkan id",
    responses={
        200: {
            "description": "Daftar barang berhasil diambil",
            "content": {
                "application/json": {
                    "example": {
                        "status": "Success",
                        "message": "Data barang berdasarkan ID berhasil diambil",
                        "data": {
                            "item_id": "I42134",
                            "name": "Mouse",
                            "price": 150000,
                            "stock": 30,
                        },
                    }
                }
            },
        }
    },
)
async def get_item_by_id(item_id: str):
    command = GetItemCommand(item_id)
    item = handler.run(command)
    return BaseResponse(
        status="Success",
        message="Data barang berdasarkan ID berhasil diambil",
        data=item,
    )


@router.post(
    "/",
    response_model=BaseResponse[Item],
    summary="Menambah item baru",
    status_code=201,
    responses={
        201: {
            "description": "Item berhasil ditambahkan",
            "content": {
                "application/json": {
                    "example": {
                        "status": "Success",
                        "message": "Barang berhasil ditambahkan",
                        "data": {
                            "item_id": "I07707",
                            "name": "Botol",
                            "price": 10000,
                            "stock": 100,
                        },
                    }
                }
            },
        },
        400: {"description": "Harga tidak boleh negatif"},
    },
)
async def add_item(item_create: ItemCreate):
    command = CreateItemCommand(item_create)
    new_item = handler.run(command)
    return BaseResponse(
        status="Success", message="Barang berhasil ditambahkan", data=new_item
    )

@router.put(
    "/{item_id}",
    response_model=BaseResponse[Item],
    summary="Mengubah data item",
    responses={
        200: {
            "description": "Daftar barang berhasil diupdate",
            "content": {
                "application/json": {
                    "example": {
                        "status": "Success",
                        "message": "Data barang berhasil diubah",
                        "data": {
                            "item_id": "I07707",
                            "name": "botol",
                            "price": 12000,
                            "stock": 120,
                        },
                    }
                }
            },
        },
        400: {"description": "Harga tidak boleh negatif"},
    },
)
async def update_item(item_id: str, item_updated: ItemCreate):
    command = UpdateItemCommand(item_id, item_updated)
    updated_item = handler.run(command)
    return BaseResponse(
        status="Success", message="Data barang berhasil diubah", data=updated_item
    )

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
async def delete_item(item_id: str):
    command = DeleteItemCommand(item_id)
    return handler.run(command)
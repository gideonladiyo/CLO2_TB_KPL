from fastapi import APIRouter, Path, Query
from typing import List
from app.models import BaseResponse, Order, OrderCreate
from app.handlers.command_handler import CommandHandler
from app.commands.order_command import (
    GetAllOrdersCommand,
    GetOrderByIdCommand,
    GetOrdersByStatusCommand,
    CreateOrderCommand,
    ChangeOrderStatusCommand,
)

router = APIRouter(prefix="/order", tags=["Order"])
handler = CommandHandler()

@router.get(
    "/",
    response_model=BaseResponse[List[Order]],
    summary="Ambil semua order"
)
async def get_all_orders():
    command = GetAllOrdersCommand()
    orders = handler.run(command)
    return BaseResponse(
        status="Success",
        message="Semua data pesanan berhasil diambil",
        data=orders,
    )

@router.get(
    "/{order_id}",
    response_model=BaseResponse[Order],
    summary="Ambil detail order berdasarkan ID"
)
async def get_order_by_id(order_id: str = Path(..., description="ID dari order")):
    command = GetOrderByIdCommand(order_id)
    order = handler.run(command)
    return BaseResponse(
        status="Success",
        message="Data pesanan berhasil diambil",
        data=order,
    )

@router.get(
    "/status/",
    response_model=BaseResponse[List[Order]],
    summary="Ambil order berdasarkan status"
)
async def get_orders_by_status(status: str = Query(..., description="Status order seperti 'pending', 'completed'")):
    command = GetOrdersByStatusCommand(status)
    orders = handler.run(command)
    return BaseResponse(
        status="Success",
        message=f"Data pesanan dengan status '{status}' berhasil diambil",
        data=orders,
    )

@router.post(
    "/",
    response_model=BaseResponse[Order],
    status_code=201,
    summary="Buat pesanan baru"
)
async def create_order(order_data: OrderCreate):
    command = CreateOrderCommand(order_data)
    new_order = handler.run(command)
    return BaseResponse(
        status="Success",
        message="Pesanan berhasil dibuat",
        data=new_order,
    )

@router.put(
    "/{order_id}/status",
    response_model=BaseResponse[Order],
    summary="Ubah status order berdasarkan trigger"
)
async def change_order_status(
    order_id: str = Path(..., description="ID pesanan"),
    trigger: str = Query(..., description="Trigger status baru (e.g., 'process', 'complete')"),
):
    command = ChangeOrderStatusCommand(order_id, trigger)
    updated_order = handler.run(command)
    return BaseResponse(
        status="Success",
        message="Status pesanan berhasil diubah",
        data=updated_order,
    )
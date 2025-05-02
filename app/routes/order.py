from fastapi import APIRouter, Query
from app.helper.order_service import order_service
from typing import List
from app.models import *

router = APIRouter(prefix="/order", tags=["Order"])


@router.get(
    "/",
    response_model=BaseResponse[List[Order]],
    summary="Ambil daftar semua pesanan",
    description="""
Endpoint ini digunakan untuk mengambil seluruh data pesanan yang tersedia di sistem.
Pesanan yang dikembalikan berisi informasi seperti:
- ID pesanan
- Daftar item yang dipesan
- Status pesanan saat ini (contoh: NEW, PAID, SHIPPED, DELIVERED)
- Waktu pembuatan dan pembaruan terakhir

Gunakan endpoint ini untuk menampilkan semua riwayat atau daftar pesanan pelanggan.
""",
    responses={
        200: {
            "description": "Daftar pesanan berhasil diambil",
            "content": {
                "application/json": {
                    "example": {
                        "status": "Success",
                        "message": "Data pesanan berhasil diambil",
                        "data": [
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
                        ],
                    }
                }
            },
        }
    },
)
def get_all_orders():
    orders = order_service.get_all_orders()
    return BaseResponse(
        status="Success", message="Data pesanan berhasil diambil", data=orders
    )


@router.get(
    "/status/{status}",
    response_model=BaseResponse[List[Order]],
    summary="Mengambil data pesanan berdasarkan status",
    description="""
    Mengambil data pesanan berdasarkan status pesanan yaitu NEW, PAID, CANCEL, SHIPPED, DELIVERED
    """,
)
def get_order_satistic(status: str):
    order_stats = order_service.get_order_stats(status=status)
    return BaseResponse(
        status="Success",
        message="Berhasil mengambil statistik pesanan",
        data=order_stats,
    )


@router.get(
    "/{id}",
    response_model=BaseResponse[Order],
    summary="Ambil detail pesanan berdasarkan ID",
    description="""
Endpoint ini digunakan untuk mengambil informasi lengkap dari satu pesanan berdasarkan ID yang diberikan.
Data yang dikembalikan mencakup:
- ID pesanan
- Daftar item dan jumlah yang dipesan
- Status saat ini (contoh: NEW, PAID, SHIPPED, DELIVERED)
- Waktu dibuat dan diperbarui terakhir

Contoh penggunaan:
`GET /order/O51354`
""",
    responses={
        200: {
            "description": "Detail pesanan berhasil ditemukan",
            "content": {
                "application/json": {
                    "example": {
                        "status": "Success",
                        "message": "Data pesanan berdasarkan ID berhasil diambil",
                        "data": {
                            "id": "O51353",
                            "items": [
                                {"item_id": "I23456", "quantity": 2},
                                {"item_id": "I34567", "quantity": 1},
                            ],
                            "status": "NEW",
                            "created_at": "2025-04-28T10:15:00",
                            "updated_at": "2025-04-28T10:15:00",
                        },
                    }
                }
            },
        },
        404: {
            "description": "Pesanan tidak ditemukan",
            "content": {
                "application/json": {
                    "example": {"detail": "Pesanan dengan ID tersebut tidak ditemukan"}
                }
            },
        },
    },
)
def get_order_by_id(id: str):
    order = order_service.get_order(id)
    return BaseResponse(
        status="Success",
        message="Data pesanan berdasarkan ID berhasil diambil",
        data=order,
    )


@router.post(
    "/",
    response_model=BaseResponse[Order],
    summary="Buat pesanan baru",
    description="""
    Membuat pesanan dengan daftar item dan jumlah masing-masing.
    """,
    status_code=201,
    responses={
        201: {
            "description": "Pesanan berhasil dibuat",
            "content": {
                "application/json": {
                    "example": {
                        "status": "Success",
                        "message": "Pesanan berhasil dibuat",
                        "data": {
                            "id": "O61848",
                            "items": [{"item_id": "I42134", "quantity": 2}],
                            "status": "NEW",
                            "created_at": "2025-05-01T04:24:54.646025",
                            "updated_at": "2025-05-01T04:24:54.646025",
                        },
                    }
                }
            },
        }
    },
)
def create_order(order_create: OrderCreate):
    new_order = order_service.create_order(order_create)
    return BaseResponse(
        status="Success", message="Pesanan berhasil dibuat", data=new_order
    )


@router.post(
    "/{id}/pay",
    response_model=BaseResponse[Order],
    summary="Mengubah status pesanan menjadi PAID",
    description="""
    Melakukan pembayaran terhadap pesanan dengan ID tertentu.

    Hanya pesanan dengan status `NEW` yang dapat dibatalkan. Jika status saat ini tidak memungkinkan transisi ke `CANCELED`, maka akan menghasilkan kesalahan 422.
    """,
    status_code=201,
    responses={
        201: {
            "description": "Pesanan berhasil dibayar",
            "content": {
                "application/json": {
                    "example": {
                        "status": "Success",
                        "message": "Pesanan berhasil dibayar",
                        "data": {
                            "id": "O61848",
                            "items": [{"item_id": "I42134", "quantity": 2}],
                            "status": "PAID",
                            "created_at": "2025-05-01T04:24:54.646025",
                            "updated_at": "2025-05-01T04:25:56.024937",
                        },
                    }
                }
            },
        },
        404: {
            "description": "Pesanan tidak ditemukan",
            "content": {
                "application/json": {
                    "example": {"detail": "Order with id 'O12345' not found"}
                }
            },
        },
        422: {
            "description": "Transisi status tidak valid",
            "content": {
                "application/json": {
                    "example": {"detail": "Invalid transition from PAID using PAY"}
                }
            },
        },
    },
)
def pay_order(id: str):
    order_service.change_order_state(id=id, trigger="PAY")
    updated_order = order_service.get_order(id=id)
    return BaseResponse(
        status="Success", message="Pesanan berhasil dibayar", data=updated_order
    )


@router.post(
    "/{id}/cancel",
    response_model=BaseResponse[Order],
    summary="Mengubah status pesanan menjadi CANCEL",
    description="""
    Melakukan pembayaran terhadap pesanan dengan ID tertentu.

    Hanya pesanan dengan status `NEW` yang dapat dibayar. Jika status saat ini tidak memungkinkan transisi ke `PAID`, maka akan menghasilkan kesalahan 422.
    """,
    status_code=201,
    responses={
        201: {
            "description": "Pesanan berhasil dibatalkan",
            "content": {
                "application/json": {
                    "example": {
                        "status": "Success",
                        "message": "Pesanan berhasil dibayar",
                        "data": {
                            "id": "O61848",
                            "items": [{"item_id": "I42134", "quantity": 2}],
                            "status": "CANCEL",
                            "created_at": "2025-05-01T04:24:54.646025",
                            "updated_at": "2025-05-01T04:25:56.024937",
                        },
                    }
                }
            },
        },
        404: {
            "description": "Pesanan tidak ditemukan",
            "content": {
                "application/json": {
                    "example": {"detail": "Order with id 'O12345' not found"}
                }
            },
        },
        422: {
            "description": "Transisi status tidak valid",
            "content": {
                "application/json": {
                    "example": {"detail": "Invalid transition from PAID using CANCEL"}
                }
            },
        },
    },
)
def cancel_order(id: str):
    order_service.change_order_state(id=id, trigger="CANCEL")
    updated_order = order_service.get_order(id=id)
    BaseResponse(
        status="Success", message="Pesanan berhasil dibatalkan", data=updated_order
    )


@router.post(
    "/{id}/ship",
    response_model=BaseResponse[Order],
    summary="Mengubah status pesanan menjadi SHIPPED",
    description="""
    Melakukan pembayaran terhadap pesanan dengan ID tertentu.

    Hanya pesanan dengan status `PAID` yang dapat dikirim. Jika status saat ini tidak memungkinkan transisi ke `SHIPPED`, maka akan menghasilkan kesalahan 422.
    """,
    status_code=201,
    responses={
        201: {
            "description": "Pesanan berhasil dikirim",
            "content": {
                "application/json": {
                    "status": "Success",
                    "message": "Pesanan berhasil dibayar",
                    "data": {
                        "id": "O61848",
                        "items": [{"item_id": "I42134", "quantity": 2}],
                        "status": "SHIPPED",
                        "created_at": "2025-05-01T04:24:54.646025",
                        "updated_at": "2025-05-01T04:25:56.024937",
                    },
                }
            },
        },
        404: {
            "description": "Pesanan tidak ditemukan",
            "content": {
                "application/json": {
                    "example": {"detail": "Order with id 'O12345' not found"}
                }
            },
        },
        422: {
            "description": "Transisi status tidak valid",
            "content": {
                "application/json": {
                    "example": {"detail": "Invalid transition from NEW using SHIP"}
                }
            },
        },
    },
)
def ship_order(id: str):
    order_service.change_order_state(id=id, trigger="SHIP")
    updated_order = order_service.get_order(id=id)
    BaseResponse(
        status="Success", message="Pesanan berhasil dikirim", data=updated_order
    )


@router.post(
    "/{id}/complete",
    response_model=BaseResponse[Order],
    summary="Mengubah status pesanan menjadi DELIVERED",
    description="""
    Melakukan pembayaran terhadap pesanan dengan ID tertentu.

    Hanya pesanan dengan status `PAID` yang dapat diselesaikan. Jika status saat ini tidak memungkinkan transisi ke `DELIVERED`, maka akan menghasilkan kesalahan 422.
    """,
    status_code=201,
    responses={
        201: {
            "description": "Pesanan berhasil diterima",
            "content": {
                "application/json": {
                    "example": {
                        "status": "Success",
                        "message": "Pesanan berhasil dibayar",
                        "data": {
                            "id": "O61848",
                            "items": [{"item_id": "I42134", "quantity": 2}],
                            "status": "DELIVERED",
                            "created_at": "2025-05-01T04:24:54.646025",
                            "updated_at": "2025-05-01T04:25:56.024937",
                        },
                    }
                }
            },
        },
        404: {
            "description": "Pesanan tidak ditemukan",
            "content": {
                "application/json": {
                    "example": {"detail": "Order with id 'O12345' not found"}
                }
            },
        },
        422: {
            "description": "Transisi status tidak valid",
            "content": {
                "application/json": {
                    "example": {"detail": "Invalid transition from PAID using COMPLETE"}
                }
            },
        },
    },
)
def complete_order(id: str):
    order_service.change_order_state(id=id, trigger="DELIVER")
    updated_order = order_service.get_order(id=id)
    BaseResponse(
        status="Success", message="Pesanan berhasil diterima", data=updated_order
    )
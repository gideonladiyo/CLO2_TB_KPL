from fastapi import APIRouter, Query
from app.helper.order_service import order_service
from typing import List
from app.models import *

router = APIRouter(prefix="/order", tags=["Order"])


@router.get(
    "/",
    response_model=List[Order],
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
def get_all_orders():
    return order_service.get_all_orders()


@router.get(
    "/{id}",
    response_model=Order,
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
                        "id": "O51354",
                        "items": [{"item_id": "I45678", "quantity": 3}],
                        "status": "PAID",
                        "created_at": "2025-04-28 11:30:22.543210",
                        "updated_at": "2025-04-28 12:05:17.987654",
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
    return order_service.get_order(id)

@router.post(
    "/",
    response_model=Order,
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


@router.post(
    "/{id}/pay",
    response_model=Order,
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
                        "id": "O12345",
                        "items": [{"item_id": "I45678", "quantity": 3}],
                        "status": "PAID",
                        "created_at": "2025-04-28 13:00:00.000000",
                        "updated_at": "2025-04-28 13:00:00.000000",
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
    return order_service.get_order(id=id)


@router.post(
    "/{id}/cancel",
    response_model=Order,
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
                        "id": "O12345",
                        "items": [{"item_id": "I45678", "quantity": 3}],
                        "status": "PAID",
                        "created_at": "2025-04-28 13:00:00.000000",
                        "updated_at": "2025-04-28 13:00:00.000000",
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
    return order_service.get_order(id=id)


@router.post(
    "/{id}/ship",
    response_model=Order,
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
                    "example": {
                        "id": "O12345",
                        "items": [{"item_id": "I45678", "quantity": 3}],
                        "status": "PAID",
                        "created_at": "2025-04-28 13:00:00.000000",
                        "updated_at": "2025-04-28 13:00:00.000000",
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
                    "example": {"detail": "Invalid transition from NEW using SHIP"}
                }
            },
        },
    },
)
def ship_order(id: str):
    order_service.change_order_state(id=id, trigger="SHIP")
    return order_service.get_order(id=id)


@router.post(
    "/{id}/complete",
    response_model=Order,
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
                        "id": "O12345",
                        "items": [{"item_id": "I45678", "quantity": 3}],
                        "status": "PAID",
                        "created_at": "2025-04-28 13:00:00.000000",
                        "updated_at": "2025-04-28 13:00:00.000000",
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
    return order_service.get_order(id=id)


# @router.patch(
#     "/{id}/status",
#     response_model=Order,
#     summary="Mengubah status pesanan berdasarkan trigger input",
#     description="""
# Mengubah status pesanan berdasarkan trigger yang diberikan.

# Trigger yang valid: `PAY`, `CANCEL`, `SHIP`, `DELIVER`.

# Jika transisi status tidak valid untuk kondisi saat ini, maka akan menghasilkan HTTP 422.
# """,
#     responses={
#         200: {
#             "description": "Status pesanan berhasil diubah",
#             "content": {
#                 "application/json": {
#                     "example": {
#                         "id": "O12345",
#                         "items": [{"item_id": "I45678", "quantity": 3}],
#                         "status": "PAID",
#                         "created_at": "2025-04-28 13:00:00.000000",
#                         "updated_at": "2025-04-28 13:05:00.000000",
#                     }
#                 }
#             },
#         },
#         404: {
#             "description": "Pesanan tidak ditemukan",
#             "content": {
#                 "application/json": {
#                     "example": {"detail": "Order with id 'O12345' not found"}
#                 }
#             },
#         },
#         400: {
#             "description": "Trigger tidak valid",
#             "content": {
#                 "application/json": {"example": {"detail": "Invalid trigger: PAYX"}}
#             },
#         },
#         422: {
#             "description": "Transisi status tidak diperbolehkan",
#             "content": {
#                 "application/json": {
#                     "example": {"detail": "Invalid transition from SHIPPED using PAY"}
#                 }
#             },
#         },
#     },
# )
# def change_order_status(
#     id: str,
#     trigger: str = Query(
#         ..., description="Trigger status (misal: PAY, CANCEL, SHIP, DELIVER)"
#     ),
# ):
#     order_service.change_order_state(id=id, trigger=trigger.upper())
#     return order_service.get_order(id=id)
# from fsm.order_fsm import *

# current_status = "NEW"
# trigger = "PAY"

# new_state = change_order_state(current_status, trigger)
# print(new_state)
# print(new_state.name)

from fastapi import FastAPI
from app.routes import item, order
from app.config import settings

app = FastAPI(
    title=settings.app_name,
    description="API untuk mengelola data produk dan pesanan.",
    version=settings.app_version,
    debug=settings.debug,
    openapi_tags=[
        {
            "name": "Item",
            "description": "Item endpoint",
        },
        {
            "name": "Order",
            "description": "Order endpoint",
        },
    ],
)

app.include_router(item.router)
app.include_router(order.router)
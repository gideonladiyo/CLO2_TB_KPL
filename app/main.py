from fastapi import FastAPI
from app.routes import item, order
from app.config import settings
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request  

class MaintenanceMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        print(settings.maintenance_mode)
        if settings.maintenance_mode:
            if request.url.path.startswith("/item") or request.url.path.startswith("/order"):
                return JSONResponse(
                    status_code=503,
                    content={
                        "detail": "Service sedang dalam maintenance"
                    }
                )
        return await call_next(request)
    

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

app.add_middleware(MaintenanceMiddleware)

app.include_router(item.router)
app.include_router(order.router)
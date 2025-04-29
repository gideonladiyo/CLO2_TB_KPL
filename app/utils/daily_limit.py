from datetime import datetime, date
from fastapi import HTTPException
from app.config import settings
from typing import List

def check_limit(orders: list):
    count = 0
    today = date.today()
    for order in orders:
        try:
            order_date = datetime.strptime(order["created_at"], "%Y-%m-%d %H:%M:%S.%f").date()
            if order_date == today:
                count += 1
        except (KeyError, ValueError):
            continue
    if count == settings.max_orders_per_day:
        raise HTTPException(status_code=429, detail="Order sudah mencapai limit")



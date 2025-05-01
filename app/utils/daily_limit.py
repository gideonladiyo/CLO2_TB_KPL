from datetime import datetime, date
from fastapi import HTTPException
from typing import List

def check_limit_order(orders_date: List, max_order:int):
    count = 0
    today = date.today()
    print(f"today date: {today}")
    print(f"max order: {max_order}")
    for order_date in orders_date:
        try:
            order_date = order_date.split(" ")[0]
            order_date = datetime.strptime(order_date, "%Y-%m-%d").date()
            print(f"order date: {order_date}")
            if order_date == today:
                count += 1
        except (KeyError, ValueError):
            continue
    if count >= max_order:
        raise HTTPException(status_code=429, detail="Order sudah mencapai limit")
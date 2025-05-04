from app.utils.stock_price_validation import validate_item
from fastapi import HTTPException

class DummyItem:
    def __init__(self, price, stock):
        self.price = price
        self.stock = stock

def test_validate_item_pass():
    item = DummyItem(price=100, stock=10)
    validate_item(item)

def test_validate_item_fail():
    item = DummyItem(price=-1, stock=10)
    try:
        validate_item(item)
        assert False, "Harusnya error karena harga negatif"
    except HTTPException as e:
        assert e.status_code == 422

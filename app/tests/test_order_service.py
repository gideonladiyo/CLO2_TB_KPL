import pytest
import os
import json
from fastapi import HTTPException
from app.helper.order_service import OrderService
from app.models import OrderCreate, OrderItemCreate
from app.fsm.order_fsm import OrderState

TEST_ORDER_PATH = "test_orders.json"


@pytest.fixture
def temp_order_service(monkeypatch):
    dummy_orders = []
    with open(TEST_ORDER_PATH, "w") as f:
        json.dump(dummy_orders, f)

    monkeypatch.setattr(
        "app.helper.order_service.file_path.ORDERS_PATH", TEST_ORDER_PATH
    )
    service = OrderService()
    yield service

    os.remove(TEST_ORDER_PATH)


def test_create_order_success(temp_order_service, monkeypatch):
    dummy_items = [{"item_id": "I0001", "name": "Item1", "price": 1000, "stock": 10}]

    monkeypatch.setattr(
        "app.helper.order_service.item_service.get_item", lambda id: dummy_items[0]
    )
    monkeypatch.setattr(
        "app.helper.order_service.item_service.buy_item", lambda id, qty: None
    )

    order_data = OrderCreate(items=[OrderItemCreate(item_id="I0001", quantity=2)])
    new_order = temp_order_service.create_order(order_data)

    assert new_order["status"] == "NEW"
    assert new_order["items"][0]["item_id"] == "I0001"


def test_get_order_not_found(temp_order_service):
    with pytest.raises(HTTPException) as exc_info:
        temp_order_service.get_order("O9999")
    assert exc_info.value.status_code == 404


def test_change_order_state_success(temp_order_service, monkeypatch):
    order_data = {
        "id": "O0001",
        "items": [],
        "status": "NEW",
        "created_at": "2025-05-01 00:00:00",
        "updated_at": "2025-05-01 00:00:00",
    }
    temp_order_service.orders.append(order_data)
    monkeypatch.setattr(
        "app.helper.order_service.change_order_state",
        lambda current_state, trigger: OrderState.PAID,
    )

    temp_order_service.change_order_state("O0001", "pay")
    updated_order = temp_order_service.get_order("O0001")

    assert updated_order["status"] == "PAID"

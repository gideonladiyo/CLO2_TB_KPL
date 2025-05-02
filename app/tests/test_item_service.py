import pytest
import os
import json
from fastapi import HTTPException
from app.helper.item_service import ItemService
from app.models import ItemCreate
from unittest.mock import patch

TEST_ITEM_PATH = "test_items.json"


@pytest.fixture
def temp_item_service(monkeypatch):
    dummy_items = [
        {"item_id": "I00001", "name": "Item A", "price": 10000, "stock": 10},
        {"item_id": "I00002", "name": "Item B", "price": 20000, "stock": 5},
    ]
    with open(TEST_ITEM_PATH, "w") as f:
        json.dump(dummy_items, f)

    monkeypatch.setattr("app.helper.item_service.file_path.ITEMS_PATH", TEST_ITEM_PATH)
    service = ItemService()
    yield service

    os.remove(TEST_ITEM_PATH)


def test_get_all_items(temp_item_service):
    items = temp_item_service.get_all_items()
    assert len(items) == 2


def test_get_item_success(temp_item_service):
    item = temp_item_service.get_item("I00001")
    assert item["name"] == "Item A"


def test_get_item_not_found(temp_item_service):
    with pytest.raises(HTTPException) as exc_info:
        temp_item_service.get_item("I99999")
    assert exc_info.value.status_code == 404


def test_create_item(temp_item_service, monkeypatch):
    item_data = ItemCreate(name="Item C", price=30000, stock=15)

    monkeypatch.setattr(
        "app.helper.item_service.generate_random_id", lambda ids, **kwargs: "I00003"
    )
    monkeypatch.setattr("app.helper.item_service.validate_item", lambda item: None)

    result = temp_item_service.create_item(item_data)

    assert result["item_id"] == "I00003"
    assert result["name"] == "Item C"


def test_update_item_success(temp_item_service, monkeypatch):
    item_update = ItemCreate(name="Updated A", price=15000, stock=8)
    monkeypatch.setattr("app.helper.item_service.validate_item", lambda item: None)

    temp_item_service.update_item("I00001", item_update)
    assert temp_item_service.items[0]["name"] == "Updated A"


def test_update_item_not_found(temp_item_service):
    item_update = ItemCreate(name="X", price=1000, stock=1)
    with pytest.raises(HTTPException) as exc_info:
        temp_item_service.update_item("I99999", item_update)
    assert exc_info.value.status_code == 404


def test_delete_item_success(temp_item_service):
    msg = temp_item_service.delete_item("I00002")
    assert msg["message"] == "Item dengan id I00002 telah dihapus"
    assert len(temp_item_service.items) == 1


def test_buy_item_success(temp_item_service):
    temp_item_service.buy_item("I00001", 2)
    assert temp_item_service.items[0]["stock"] == 8


def test_buy_item_insufficient_stock(temp_item_service):
    with pytest.raises(HTTPException) as exc_info:
        temp_item_service.buy_item("I00002", 10)
    assert exc_info.value.status_code == 400

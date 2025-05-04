from fastapi.testclient import TestClient
from app.main import app
from typing import List
from app.models import *
from app.utils.file_path import file_path
from app.fsm.order_fsm import *
import json

client = TestClient(app)


def test_get_orders():
    response = client.get("/order/")
    assert response.status_code == 200
    data = response.json()["data"]
    for order in data:
        assert isinstance(order, dict)
        assert order["id"].startswith("O")
        for item in order["items"]:
            assert isinstance(item, dict)
            assert "item_id" in item
            assert item["item_id"].startswith("I")
            assert "quantity" in item
            assert item["quantity"] > 0
        assert order["status"] in [state.name for state in OrderState]
        assert datetime.fromisoformat(order["created_at"])
        assert datetime.fromisoformat(order["updated_at"])


def test_get_order():
    with open(file_path.ORDERS_PATH, "r") as f:
        data = json.load(f)
    order_id = data[0]["id"]
    response = client.get(f"/order/{order_id}")
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["id"] == order_id
    assert data["status"] in [state.name for state in OrderState]
    assert datetime.fromisoformat(data["created_at"])
    assert datetime.fromisoformat(data["updated_at"])


def test_get_not_found():
    response = client.get("/order/1234567890")
    assert response.status_code == 404


def test_create_order():
    with open(file_path.ITEMS_PATH, "r") as f:
        item_data = json.load(f)
    items = [
        {"item_id": item_data[0]["item_id"], "quantity": 5},
        {"item_id": item_data[1]["item_id"], "quantity": 5},
    ]
    new_order = {"items": items}
    response = client.post("/order/", json=new_order)
    assert response.status_code == 201
    data = response.json()["data"]
    assert data["id"].startswith("O")
    assert data["status"] in [state.name for state in OrderState]
    for item in data["items"]:
        assert item["quantity"] == 5
    assert datetime.fromisoformat(data["created_at"])
    assert datetime.fromisoformat(data["updated_at"])

def test_create_failed():
    with open(file_path.ITEMS_PATH, "r") as f:
        item_data = json.load(f)
    items = [
        {"item_id": item_data[0]["item_id"], "quantity": 10000},
        {"item_id": item_data[1]["item_id"], "quantity": 10000},
    ]
    new_order = {"items": items}
    response = client.post("/order/", json=new_order)
    assert response.status_code == 400
    new_order = {"items": []}
    response = client.post("/order/", json=new_order)
    assert response.status_code == 400

def test_order_flow():
    with open(file_path.ORDERS_PATH, "r") as f:
        order_data = json.load(f)
    last_order = order_data[-1]
    print(last_order)

    # cancel
    response = client.post(f"/order/{last_order['id']}/cancel")
    assert response.status_code == 201
    assert response.json()["data"]["status"] == "CANCELED"
    assert response.json()["data"]["status"] in [state.name for state in OrderState]

    # ke state pay pasti pasti gagal
    response = client.post(f"/order/{last_order['id']}/pay")
    assert response.status_code == 422

    # buat order baru
    with open(file_path.ITEMS_PATH, "r") as f:
        item_data = json.load(f)
    items = [
        {"item_id": item_data[0]["item_id"], "quantity": 5},
        {"item_id": item_data[1]["item_id"], "quantity": 5},
    ]
    new_order = {"items": items}
    response = client.post("/order/", json=new_order)
    print(response)
    assert response.status_code == 201

    # pay
    with open(file_path.ORDERS_PATH, "r") as f:
        order_data = json.load(f)
    last_order = order_data[-1]
    response = client.post(f"/order/{last_order['id']}/pay")
    assert response.status_code == 201
    assert response.json()["data"]["status"] == "PAID"
    assert response.json()["data"]["status"] in [state.name for state in OrderState]

    # ship
    response = client.post(f"/order/{last_order['id']}/ship")
    assert response.status_code == 201
    assert response.json()["data"]["status"] == "SHIPPED"
    assert response.json()["data"]["status"] in [state.name for state in OrderState]

    # delivered
    response = client.post(f"/order/{last_order['id']}/complete")
    assert response.status_code == 201
    assert response.json()["data"]["status"] == "DELIVERED"
    assert response.json()["data"]["status"] in [state.name for state in OrderState]
    
    # Delete Order Test Data
    with open(file_path.ORDERS_PATH, "r") as f:
        data = json.load(f)
    data.pop()
    data.pop()
    with open(file_path.ORDERS_PATH, "w") as f:
        json.dump(data, f, indent=4)
    
    # Set Item Stock Back to Original
    with open(file_path.ITEMS_PATH, "r") as f:
        items = json.load(f)
    items[0]["stock"] += 10
    items[1]["stock"] += 10
    with open(file_path.ITEMS_PATH, "w") as f:
        json.dump(items, f, indent=4)
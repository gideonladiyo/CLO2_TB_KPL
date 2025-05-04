from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_items():
    response = client.get("/item/")
    assert response.status_code == 200
    data = response.json()["data"]

    for item in data:
        assert "item_id" in item
        assert item["item_id"].startswith("I")
        assert "name" in item
        assert "price" in item
        assert item["price"] > 0
        assert "stock" in item
        assert item["stock"] > 0

def test_create_item():
    new_item = {"name": "Item B", "price": 20000, "stock": 10}
    response = client.post("/item/", json=new_item)
    assert response.status_code == 201
    data = response.json()["data"]
    assert "item_id" in data
    assert data["item_id"].startswith("I")
    assert "name" in data
    assert data["name"] == "Item B"
    assert "price" in data
    assert data["price"] > 0
    assert "stock" in data
    assert data["stock"] > 0

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_items():
    response = client.get("/item/")
    assert response.status_code == 200
    data = response.json()["data"]

    for item in data:
        assert item["item_id"].startswith("I")
        assert len(item["name"]) > 0
        assert item["price"] > 0
        assert item["stock"] > 0

def test_get_item():
    response = client.get("/item/I93412")
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["item_id"] == "I93412"
    assert len(data["name"]) > 0
    assert data["price"] > 0
    assert data["stock"] > 0

def test_item_not_found():
    response = client.get("/item/I1234567")
    assert response.status_code == 404

def test_create_item():
    new_item = {"name": "Item B", "price": 20000, "stock": 10}
    response = client.post("/item/", json=new_item)
    assert response.status_code == 201
    data = response.json()["data"]
    assert data["item_id"].startswith("I")
    assert data["name"] == "Item B"
    assert data["price"] == 20000
    assert data["stock"] == 10

def test_create_item_failed():
    item1 = {"name": "Item B", "price": -1, "stock": 10}
    response = client.post("/item/", json=item1)
    assert response.status_code == 422
    assert response.json()["detail"] == "Price tidak boleh negatif"
    item2 = {"name": "Item B", "price": 20000, "stock": -1}
    response = client.post("/item/", json=item2)
    assert response.status_code == 422
    assert response.json()["detail"] == "Stock tidak boleh negatif"

def test_update_item():
    last_item = client.get("/item/")
    assert last_item.status_code == 200
    last_item = last_item.json()["data"][-1]
    updated_item = {"name": "Updated Item B", "price": 10000, "stock": 20}
    response = client.put(f"/item/{last_item['item_id']}", json=updated_item)
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["item_id"].startswith("I")
    assert data["name"] == "Updated Item B"
    assert data["price"] == 10000
    assert data["stock"] == 20

def test_update_failed():
    item = client.get("/item/")
    assert item.status_code == 200
    last_item = item.json()["data"][-1]
    updated_item_1 = {"name": "Updated Item B", "price": -1, "stock": 20}
    response = client.put(f"/item/{last_item['item_id']}", json=updated_item_1)
    assert response.status_code == 422
    assert response.json()["detail"] == "Price tidak boleh negatif"
    updated_item_2 = {"name": "Updated Item B", "price": 20000, "stock": -1}
    response = client.put(f"/item/{last_item['item_id']}", json=updated_item_2)
    assert response.status_code == 422
    assert response.json()["detail"] == "Stock tidak boleh negatif"

def test_delete_item():
    last_item = client.get("/item/")
    assert last_item.status_code == 200
    last_item = last_item.json()["data"][-1]
    response = client.delete(f"/item/{last_item['item_id']}")
    assert response.status_code == 200
    deleted_item = client.get(f"/item/{last_item['item_id']}")
    assert deleted_item.status_code == 404

def test_delete_not_found():
    response = client.delete("/item/1234567890")
    assert response.status_code == 404
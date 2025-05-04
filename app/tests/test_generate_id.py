from app.utils.generate_id import generate_random_id

def test_generate_random_id():
    existing_ids = ["ORD00001", "ORD00002"]
    new_id = generate_random_id(existing_ids, "ORD", 5)
    assert new_id not in existing_ids
    assert new_id.startswith("ORD")
    assert len(new_id) == 8

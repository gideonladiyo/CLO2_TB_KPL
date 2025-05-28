import os
from app.utils.file_path import Path


class TestPath:
    def test_base_dir_exists(self):
        assert os.path.isdir(Path.BASE_DIR)

    def test_base_dir_normalized(self):
        assert Path.BASE_DIR == os.path.normpath(Path.BASE_DIR)

    def test_paths_construction(self):
        expected_items_path = os.path.join(Path.BASE_DIR, "data", "items.json")
        expected_orders_path = os.path.join(Path.BASE_DIR, "data", "orders.json")

        assert Path.ITEMS_PATH == expected_items_path
        assert Path.ORDERS_PATH == expected_orders_path

    def test_paths_have_json_extension(self):
        assert Path.ITEMS_PATH.endswith(".json")
        assert Path.ORDERS_PATH.endswith(".json")

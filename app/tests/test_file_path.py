import os
from app.utils.file_path import get_path_instance


class TestPathSingleton:
    def test_base_dir_exists(self):
        path = get_path_instance()
        assert os.path.isdir(path.BASE_DIR)

    def test_base_dir_normalized(self):
        path = get_path_instance()
        assert path.BASE_DIR == os.path.normpath(path.BASE_DIR)

    def test_paths_construction(self):
        path = get_path_instance()
        expected_items_path = os.path.join(path.BASE_DIR, "data", "items.json")
        expected_orders_path = os.path.join(path.BASE_DIR, "data", "orders.json")

        assert path.ITEMS_PATH == expected_items_path
        assert path.ORDERS_PATH == expected_orders_path

    def test_paths_have_json_extension(self):
        path = get_path_instance()
        assert path.ITEMS_PATH.endswith(".json")
        assert path.ORDERS_PATH.endswith(".json")
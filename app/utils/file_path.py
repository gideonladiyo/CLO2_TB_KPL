import os


class PathSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PathSingleton, cls).__new__(cls)
            cls._instance._initialize_paths()
        return cls._instance

    def _initialize_paths(self):
        self.BASE_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
        self.ITEMS_PATH = os.path.join(self.BASE_DIR, "data", "items.json")
        self.ORDERS_PATH = os.path.join(self.BASE_DIR, "data", "orders.json")


def get_path_instance():
    return PathSingleton()
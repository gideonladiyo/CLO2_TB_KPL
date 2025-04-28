import os

class Path:
    BASE_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
    
    ITEMS_PATH = os.path.join(BASE_DIR, "data", "items.json")
    ORDERS_PATH = os.path.join(BASE_DIR, "data", "orders.json")

file_path = Path()
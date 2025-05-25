import subprocess
import time
import json
import os

filepath = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "orders.json"))
item_path = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "items.json"))

def run_k6_test():
    print("Menjalankan k6 test...")

    with open (filepath, "r") as f:
        backup_orders = json.load(f)
    with open (item_path, "r") as f:
        backup_items = json.load(f)

    result = subprocess.run(
        ["k6", "run", "app/tests/performance_test/test_api_performance.js"], capture_output=True, text=True
    )
    print(result.stdout)

    with open(filepath, "w") as f:
        json.dump(backup_orders, f, indent=4)
    with open(item_path, "w") as f:
        json.dump(backup_items, f, indent=4)

    if result.returncode != 0:
        print("K6 test gagal:", result.stderr)
        return False
    return True


if __name__ == "__main__":
    if run_k6_test():
        time.sleep(2)
        print("K6 Testing success")

import os
import socket
import pytest
import requests
from xprocess import ProcessStarter

PROJECT_DIR = "/home/user/myproject"

@pytest.fixture(scope="session")
def start_app(xprocess):
    """
    Starts the encore application using xprocess. Confirms readiness via port check.
    """
    class Starter(ProcessStarter):
        name = "start_app"
        args = ["encore", "run"]
        env = os.environ.copy()
        popen_kwargs = {
            "cwd": PROJECT_DIR,
            "text": True,
        }
        timeout = 180
        terminate_on_interrupt = True

        def startup_check(self):
            """
            Returns True if port 4000 is accepting connections.
            """
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                return s.connect_ex(("localhost", 4000)) == 0

    xprocess.ensure(Starter.name, Starter)
    yield
    info = xprocess.getinfo(Starter.name)
    info.terminate()

def test_inventory_and_orders_workflow(start_app):
    """
    Test the multi-service workflow:
    1. Create a product in inventory
    2. Create an order successfully (reserves stock)
    3. Reserve stock directly
    4. Create an order that fails due to insufficient stock
    """
    base_url = "http://localhost:4000"
    
    # 1. Create Product
    inventory_url = f"{base_url}/inventory"
    product_data = {"name": "Laptop", "stock": 10}
    response = requests.post(inventory_url, json=product_data)
    assert response.status_code == 200, f"Expected 200 OK for creating product, got {response.status_code}: {response.text}"
    
    resp_json = response.json()
    assert "id" in resp_json, "Response missing 'id' field"
    assert resp_json["name"] == "Laptop", f"Expected name 'Laptop', got {resp_json.get('name')}"
    assert resp_json["stock"] == 10, f"Expected stock 10, got {resp_json.get('stock')}"
    
    product_id = resp_json["id"]
    
    # 2. Create Order (Success)
    orders_url = f"{base_url}/orders"
    order_data = {"product_id": product_id, "quantity": 3}
    response = requests.post(orders_url, json=order_data)
    assert response.status_code == 200, f"Expected 200 OK for creating order, got {response.status_code}: {response.text}"
    
    resp_json = response.json()
    assert resp_json["product_id"] == product_id, f"Expected product_id {product_id}, got {resp_json.get('product_id')}"
    assert resp_json["quantity"] == 3, f"Expected quantity 3, got {resp_json.get('quantity')}"
    assert resp_json["status"] == "created", f"Expected status 'created', got {resp_json.get('status')}"
    
    # 3. Direct Reserve (Success)
    reserve_url = f"{base_url}/inventory/{product_id}/reserve"
    reserve_data = {"quantity": 5}
    response = requests.post(reserve_url, json=reserve_data)
    assert response.status_code == 200, f"Expected 200 OK for direct reserve, got {response.status_code}: {response.text}"
    
    # 4. Create Order (Insufficient Stock)
    # Total stock was 10. We used 3 + 5 = 8. Remaining is 2. Trying to order 5 should fail.
    order_data_fail = {"product_id": product_id, "quantity": 5}
    response = requests.post(orders_url, json=order_data_fail)
    assert response.status_code == 400, f"Expected 400 Bad Request for insufficient stock, got {response.status_code}: {response.text}"

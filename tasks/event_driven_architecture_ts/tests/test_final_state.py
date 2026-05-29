import os
import time
import socket
import requests
import pytest
from xprocess import ProcessStarter

PROJECT_DIR = "/home/user/myproject"

@pytest.fixture(scope="session", autouse=True)
def npm_install():
    """Run npm install before starting the app."""
    import subprocess
    subprocess.run(["npm", "install"], cwd=PROJECT_DIR, check=True)

@pytest.fixture(scope="session")
def start_app(xprocess):
    """
    Starts the encore service using xprocess. Confirms readiness via port check.
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
            Check if port 4000 is accepting connections.
            """
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                return s.connect_ex(("localhost", 4000)) == 0

    xprocess.ensure(Starter.name, Starter)
    
    # Give Encore enough time to provision databases and start services
    time.sleep(15)
    
    yield

    info = xprocess.getinfo(Starter.name)
    info.terminate()

def test_create_order(start_app):
    """Test POST /orders to create an order."""
    url = "http://localhost:4000/orders"
    payload = {
        "id": "ord-123",
        "item": "Laptop",
        "user_email": "alice@example.com"
    }
    response = requests.post(url, json=payload)
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}. Response: {response.text}"

def test_verify_email_sent(start_app):
    """Test GET /emails/:user_email to verify the email was sent via pub/sub."""
    # Wait for the event to be processed
    time.sleep(5)
    
    url = "http://localhost:4000/emails/alice@example.com"
    response = requests.get(url)
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}. Response: {response.text}"
    
    data = response.json()
    assert "emails" in data, f"Expected 'emails' key in response JSON, got {data}"
    
    emails = data["emails"]
    assert isinstance(emails, list), "Expected 'emails' to be a list"
    
    found = False
    for email in emails:
        if email.get("user_email") == "alice@example.com" and email.get("message") == "Order created for item: Laptop":
            found = True
            break
            
    assert found, f"Expected to find email for alice@example.com with message 'Order created for item: Laptop'. Found: {emails}"

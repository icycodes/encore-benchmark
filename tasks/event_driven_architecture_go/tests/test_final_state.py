import os
import re
import time
import requests
import pytest

PROJECT_DIR = "/home/user/eda-app"

@pytest.fixture(scope="session")
def app_id():
    encore_app_path = os.path.join(PROJECT_DIR, "encore.app")
    assert os.path.isfile(encore_app_path), f"encore.app not found at {encore_app_path}"
    
    with open(encore_app_path, "r") as f:
        content = f.read()
    
    match = re.search(r'"id"\s*:\s*"([^"]+)"', content)
    assert match is not None, "Could not extract app ID from encore.app"
    return match.group(1)

@pytest.fixture(scope="session")
def base_url(app_id):
    return f"https://staging-{app_id}.encr.app"

@pytest.fixture(scope="session")
def run_id():
    run_id = os.environ.get("ZEALT_RUN_ID")
    assert run_id is not None, "ZEALT_RUN_ID environment variable is not set."
    return run_id

def test_publish_message(base_url, run_id):
    message = f"test-message-{run_id}"
    url = f"{base_url}/publish"
    payload = {"message": message}
    
    response = requests.post(url, json=payload)
    assert response.status_code == 200, f"POST /publish failed with status {response.status_code}: {response.text}"

def test_get_messages(base_url, run_id):
    # Wait for the Pub/Sub subscriber to process the message
    time.sleep(5)
    
    message = f"test-message-{run_id}"
    url = f"{base_url}/messages"
    
    response = requests.get(url)
    assert response.status_code == 200, f"GET /messages failed with status {response.status_code}: {response.text}"
    
    data = response.json()
    # Assuming the response has a list of messages, we search for the specific message
    # We don't know the exact schema, but we can convert the response to string and check if the message is in it
    assert message in response.text, f"Expected message '{message}' not found in GET /messages response: {response.text}"

import os
import re
import requests
import pytest

PROJECT_DIR = "/home/user/helloworld"

@pytest.fixture(scope="session")
def app_id():
    app_file_path = os.path.join(PROJECT_DIR, "encore.app")
    assert os.path.isfile(app_file_path), f"encore.app not found at {app_file_path}"
    
    with open(app_file_path, "r") as f:
        content = f.read()
        
    match = re.search(r'"id"\s*:\s*"([^"]+)"', content)
    assert match, "Could not find app ID in encore.app"
    return match.group(1)

@pytest.fixture(scope="session")
def base_url(app_id):
    return f"https://staging-{app_id}.encr.app"

def test_create_user(base_url, pytestconfig):
    response = requests.post(
        f"{base_url}/users",
        json={"name": "Alice", "email": "alice@example.com"}
    )
    assert response.status_code in [200, 201], f"Expected status 200/201, got {response.status_code}. Response: {response.text}"
    
    data = response.json()
    assert "id" in data, f"Expected 'id' in response, got {data}"
    assert data.get("name") == "Alice", f"Expected name 'Alice', got {data.get('name')}"
    assert data.get("email") == "alice@example.com", f"Expected email 'alice@example.com', got {data.get('email')}"
    
    # Store created_id for other tests
    pytestconfig.cache.set("created_id", data["id"])

def test_get_user(base_url, pytestconfig):
    created_id = pytestconfig.cache.get("created_id", None)
    assert created_id is not None, "created_id was not set by test_create_user"
    
    response = requests.get(f"{base_url}/users/{created_id}")
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}. Response: {response.text}"
    
    data = response.json()
    assert data.get("id") == created_id, f"Expected id {created_id}, got {data.get('id')}"
    assert data.get("name") == "Alice", f"Expected name 'Alice', got {data.get('name')}"
    assert data.get("email") == "alice@example.com", f"Expected email 'alice@example.com', got {data.get('email')}"

def test_list_users(base_url, pytestconfig):
    created_id = pytestconfig.cache.get("created_id", None)
    assert created_id is not None, "created_id was not set by test_create_user"
    
    response = requests.get(f"{base_url}/users")
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}. Response: {response.text}"
    
    data = response.json()
    assert isinstance(data, list), f"Expected response to be a list, got {type(data)}"
    
    # Verify the created user is in the list
    user_found = any(u.get("id") == created_id for u in data)
    assert user_found, f"Created user {created_id} not found in user list: {data}"

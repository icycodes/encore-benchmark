import os
import re
import requests
import pytest

PROJECT_DIR = "/home/user/mytodo"
ENCORE_APP_FILE = os.path.join(PROJECT_DIR, "encore.app")

@pytest.fixture(scope="session")
def base_url():
    assert os.path.isfile(ENCORE_APP_FILE), f"encore.app file not found at {ENCORE_APP_FILE}. Ensure the app was initialized."
    
    with open(ENCORE_APP_FILE, "r") as f:
        content = f.read()
    
    match = re.search(r'"id"\s*:\s*"([^"]+)"', content)
    assert match is not None, f"Could not extract app id from {ENCORE_APP_FILE}."
    
    app_id = match.group(1)
    return f"https://staging-{app_id}.encr.app"

def test_todo_crud_flow(base_url):
    # 1. Create Todo
    create_url = f"{base_url}/todos"
    create_payload = {"title": "Buy milk", "done": False}
    create_resp = requests.post(create_url, json=create_payload)
    assert create_resp.status_code in [200, 201], f"Failed to create todo. Status: {create_resp.status_code}, Response: {create_resp.text}"
    
    create_data = create_resp.json()
    assert "id" in create_data, f"Created todo response missing 'id' field: {create_data}"
    todo_id = create_data["id"]
    assert create_data.get("title") == "Buy milk", f"Expected title 'Buy milk', got: {create_data.get('title')}"
    
    # 2. List Todos
    list_url = f"{base_url}/todos"
    list_resp = requests.get(list_url)
    assert list_resp.status_code == 200, f"Failed to list todos. Status: {list_resp.status_code}, Response: {list_resp.text}"
    
    list_data = list_resp.json()
    # Check if the created todo is in the list
    found = any(str(todo.get("id")) == str(todo_id) for todo in list_data)
    assert found, f"Created todo with id {todo_id} not found in the list of todos."
    
    # 3. Update Todo
    update_url = f"{base_url}/todos/{todo_id}"
    update_payload = {"title": "Buy almond milk", "done": True}
    update_resp = requests.put(update_url, json=update_payload)
    assert update_resp.status_code == 200, f"Failed to update todo. Status: {update_resp.status_code}, Response: {update_resp.text}"
    
    # 4. Verify Update
    verify_update_resp = requests.get(list_url)
    assert verify_update_resp.status_code == 200, f"Failed to list todos after update. Status: {verify_update_resp.status_code}"
    
    updated_data = verify_update_resp.json()
    updated_todo = next((todo for todo in updated_data if str(todo.get("id")) == str(todo_id)), None)
    assert updated_todo is not None, f"Todo with id {todo_id} not found after update."
    assert updated_todo.get("title") == "Buy almond milk", f"Expected updated title 'Buy almond milk', got: {updated_todo.get('title')}"
    assert updated_todo.get("done") is True, f"Expected updated done status to be True, got: {updated_todo.get('done')}"
    
    # 5. Delete Todo
    delete_url = f"{base_url}/todos/{todo_id}"
    delete_resp = requests.delete(delete_url)
    assert delete_resp.status_code == 200, f"Failed to delete todo. Status: {delete_resp.status_code}, Response: {delete_resp.text}"
    
    # 6. Verify Deletion
    verify_delete_resp = requests.get(list_url)
    assert verify_delete_resp.status_code == 200, f"Failed to list todos after deletion. Status: {verify_delete_resp.status_code}"
    
    final_data = verify_delete_resp.json()
    still_exists = any(str(todo.get("id")) == str(todo_id) for todo in final_data)
    assert not still_exists, f"Todo with id {todo_id} still exists after deletion."

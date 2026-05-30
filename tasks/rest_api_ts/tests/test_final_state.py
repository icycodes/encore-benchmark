import os
import re
import requests
import pytest

def get_run_id():
    run_id = os.environ.get("ZEALT_RUN_ID")
    assert run_id, "ZEALT_RUN_ID environment variable is not set."
    return run_id

def get_app_id(run_id):
    project_dir = f"/home/user/helloworld-{run_id}"
    app_file = os.path.join(project_dir, "encore.app")
    assert os.path.isfile(app_file), f"encore.app file not found at {app_file}"
    
    with open(app_file, "r") as f:
        content = f.read()
        
    match = re.search(r'"id"\s*:\s*"([^"]+)"', content)
    assert match, f"Could not find app ID in {app_file}"
    return match.group(1)

def test_rest_api_crud():
    run_id = get_run_id()
    app_id = get_app_id(run_id)
    
    base_url = f"https://staging-{app_id}.encr.app"
    
    # 1. Create Book
    post_url = f"{base_url}/book"
    payload = {"title": "The Hobbit", "author": "Tolkien"}
    response = requests.post(post_url, json=payload)
    assert response.status_code in [200, 201], f"POST /book failed with status {response.status_code}: {response.text}"
    
    data = response.json()
    assert "id" in data, f"Response missing 'id': {data}"
    assert data.get("title") == "The Hobbit", f"Expected title 'The Hobbit', got: {data.get('title')}"
    assert data.get("author") == "Tolkien", f"Expected author 'Tolkien', got: {data.get('author')}"
    
    created_id = data["id"]
    
    # 2. Get Book by ID
    get_url = f"{base_url}/book/{created_id}"
    response = requests.get(get_url)
    assert response.status_code == 200, f"GET /book/{created_id} failed with status {response.status_code}: {response.text}"
    
    data = response.json()
    assert data.get("id") == created_id, f"Expected id {created_id}, got: {data.get('id')}"
    assert data.get("title") == "The Hobbit", f"Expected title 'The Hobbit', got: {data.get('title')}"
    assert data.get("author") == "Tolkien", f"Expected author 'Tolkien', got: {data.get('author')}"
    
    # 3. List Books
    list_url = f"{base_url}/book"
    response = requests.get(list_url)
    assert response.status_code == 200, f"GET /book failed with status {response.status_code}: {response.text}"
    
    data = response.json()
    assert isinstance(data, list), f"Expected response to be a list, got: {type(data)}"
    
    found = False
    for book in data:
        if book.get("id") == created_id:
            found = True
            assert book.get("title") == "The Hobbit"
            assert book.get("author") == "Tolkien"
            break
            
    assert found, f"Created book with id {created_id} not found in the list of books."

import os
import re
import requests
import pytest

APP_ID_FILE = "/home/user/helloworld/app_id.txt"

@pytest.fixture(scope="session")
def app_id():
    assert os.path.isfile(APP_ID_FILE), f"Log file not found at {APP_ID_FILE}"
    with open(APP_ID_FILE, "r") as f:
        content = f.read()
    
    match = re.search(r"App ID:\s*(\S+)", content)
    assert match is not None, f"Could not find 'App ID: <app_id>' in {APP_ID_FILE}. Content: {content}"
    return match.group(1)

def test_create_and_verify_book(app_id):
    base_url = f"https://staging-{app_id}.encr.app"
    
    # 1. Create Book
    post_url = f"{base_url}/books"
    post_data = {"title": "The Hobbit", "author": "Tolkien"}
    post_response = requests.post(post_url, json=post_data)
    
    assert post_response.status_code == 200, f"POST /books failed with status {post_response.status_code}. Response: {post_response.text}"
    post_json = post_response.json()
    assert "id" in post_json, f"Response missing 'id' field: {post_json}"
    assert post_json.get("title") == "The Hobbit", f"Expected title 'The Hobbit', got: {post_json.get('title')}"
    assert post_json.get("author") == "Tolkien", f"Expected author 'Tolkien', got: {post_json.get('author')}"
    
    created_id = post_json["id"]
    
    # 2. List Books
    get_url = f"{base_url}/books"
    get_response = requests.get(get_url)
    assert get_response.status_code == 200, f"GET /books failed with status {get_response.status_code}. Response: {get_response.text}"
    get_json = get_response.json()
    
    assert isinstance(get_json, list), f"Expected GET /books to return a list, got: {type(get_json)}"
    found = any(book.get("id") == created_id and book.get("title") == "The Hobbit" and book.get("author") == "Tolkien" for book in get_json)
    assert found, f"Created book not found in GET /books response: {get_json}"
    
    # 3. Delete Book
    delete_url = f"{base_url}/books/{created_id}"
    delete_response = requests.delete(delete_url)
    assert delete_response.status_code == 200, f"DELETE /books/{created_id} failed with status {delete_response.status_code}. Response: {delete_response.text}"

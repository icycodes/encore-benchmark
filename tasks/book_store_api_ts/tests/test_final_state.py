import os
import re
import requests
import pytest

PROJECT_DIR = "/home/user/bookstore"

@pytest.fixture(scope="session")
def base_url():
    app_file_path = os.path.join(PROJECT_DIR, "encore.app")
    assert os.path.isfile(app_file_path), f"encore.app not found at {app_file_path}"
    
    with open(app_file_path, "r") as f:
        content = f.read()
        
    match = re.search(r'"id"\s*:\s*"([^"]+)"', content)
    assert match is not None, "Could not extract app ID from encore.app"
    
    app_id = match.group(1)
    return f"https://staging-{app_id}.encr.app"

def test_bookstore_api_workflow(base_url):
    # Step 3: Create Book
    create_payload = {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald"}
    create_resp = requests.post(f"{base_url}/books", json=create_payload)
    assert create_resp.status_code == 200, f"Expected POST /books to return 200, got {create_resp.status_code}: {create_resp.text}"
    
    created_book = create_resp.json()
    assert created_book.get("title") == "The Great Gatsby", f"Expected title 'The Great Gatsby', got {created_book.get('title')}"
    assert created_book.get("author") == "F. Scott Fitzgerald", f"Expected author 'F. Scott Fitzgerald', got {created_book.get('author')}"
    assert "id" in created_book, "Expected 'id' in created book response"
    
    created_id = created_book["id"]
    
    # Step 4: List Books
    list_resp = requests.get(f"{base_url}/books")
    assert list_resp.status_code == 200, f"Expected GET /books to return 200, got {list_resp.status_code}: {list_resp.text}"
    
    books = list_resp.json()
    assert isinstance(books, list), f"Expected GET /books to return a list, got {type(books)}"
    
    found_book = next((b for b in books if b.get("id") == created_id), None)
    assert found_book is not None, f"Created book with id {created_id} not found in GET /books response"
    assert found_book.get("title") == "The Great Gatsby", f"Expected title 'The Great Gatsby', got {found_book.get('title')}"
    assert found_book.get("author") == "F. Scott Fitzgerald", f"Expected author 'F. Scott Fitzgerald', got {found_book.get('author')}"
    
    # Step 5: Delete Book
    delete_resp = requests.delete(f"{base_url}/books/{created_id}")
    assert delete_resp.status_code == 200, f"Expected DELETE /books/{created_id} to return 200, got {delete_resp.status_code}: {delete_resp.text}"
    
    # Step 6: Verify Deletion
    verify_resp = requests.get(f"{base_url}/books")
    assert verify_resp.status_code == 200, f"Expected GET /books to return 200, got {verify_resp.status_code}: {verify_resp.text}"
    
    books_after_delete = verify_resp.json()
    found_book_after = next((b for b in books_after_delete if b.get("id") == created_id), None)
    assert found_book_after is None, f"Book with id {created_id} was not deleted, found in GET /books response"

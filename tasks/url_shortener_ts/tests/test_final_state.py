import os
import re
import pytest
import requests

PROJECT_DIR = "/home/user/url-shortener"

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

def test_url_shortener_flow(base_url):
    # 1. Shorten a URL
    post_url = f"{base_url}/url"
    payload = {"url": "https://www.google.com"}
    
    post_response = requests.post(post_url, json=payload)
    assert post_response.status_code == 200, f"POST /url failed with status {post_response.status_code}: {post_response.text}"
    
    post_data = post_response.json()
    assert "id" in post_data, "Response missing 'id' field"
    assert "url" in post_data, "Response missing 'url' field"
    assert post_data["url"] == "https://www.google.com", f"Expected url 'https://www.google.com', got {post_data['url']}"
    
    short_id = post_data["id"]
    assert isinstance(short_id, str) and len(short_id) > 0, "short_id must be a non-empty string"
    
    # 2. Retrieve the URL
    get_url = f"{base_url}/url/{short_id}"
    get_response = requests.get(get_url)
    assert get_response.status_code == 200, f"GET /url/{short_id} failed with status {get_response.status_code}: {get_response.text}"
    
    get_data = get_response.json()
    assert "id" in get_data, "Response missing 'id' field"
    assert "url" in get_data, "Response missing 'url' field"
    assert get_data["id"] == short_id, f"Expected id '{short_id}', got {get_data['id']}"
    assert get_data["url"] == "https://www.google.com", f"Expected url 'https://www.google.com', got {get_data['url']}"

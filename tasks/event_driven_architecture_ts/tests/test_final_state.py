import os
import re
import time
import requests
import pytest

APP_DIR = "/home/user/eda_app"
ENCORE_APP_FILE = os.path.join(APP_DIR, "encore.app")

@pytest.fixture(scope="session")
def app_url():
    assert os.path.isfile(ENCORE_APP_FILE), f"encore.app not found at {ENCORE_APP_FILE}"
    
    with open(ENCORE_APP_FILE, "r") as f:
        content = f.read()
        
    match = re.search(r'"id"\s*:\s*"([^"]+)"', content)
    assert match is not None, "Could not extract app ID from encore.app"
    
    app_id = match.group(1)
    return f"https://staging-{app_id}.encr.app"

def test_publish_and_retrieve_message(app_url):
    # 1. Verify POST /publish
    publish_url = f"{app_url}/publish"
    test_message = "hello harbor"
    
    post_response = requests.post(publish_url, json={"text": test_message})
    assert post_response.status_code in (200, 201), \
        f"POST /publish failed with status {post_response.status_code}: {post_response.text}"
    
    # Wait for the Pub/Sub message to be processed and stored
    time.sleep(5)
    
    # 2. Verify GET /messages
    messages_url = f"{app_url}/messages"
    get_response = requests.get(messages_url)
    assert get_response.status_code == 200, \
        f"GET /messages failed with status {get_response.status_code}: {get_response.text}"
    
    data = get_response.json()
    
    # The response should contain the message we published
    # We don't know the exact structure, but it should contain "hello harbor"
    response_text = get_response.text
    assert test_message in response_text, \
        f"Expected message '{test_message}' not found in GET /messages response: {response_text}"

import os
import time
import requests
import pytest
import subprocess
import socket
from xprocess import ProcessStarter

PROJECT_DIR = "/home/user/myproject"
BASE_URL = "http://localhost:4000"

@pytest.fixture(scope="session")
def start_app(xprocess):
    class Starter(ProcessStarter):
        name = "encore_run"
        args = ["encore", "run"]
        env = os.environ.copy()
        popen_kwargs = {
            "cwd": PROJECT_DIR,
            "text": True,
        }
        timeout = 180
        terminate_on_interrupt = True

        def startup_check(self):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                return s.connect_ex(("localhost", 4000)) == 0

    xprocess.ensure(Starter.name, Starter)
    
    # Wait an additional 10 seconds to give Encore time to start the app and database fully
    time.sleep(10)

    yield

    info = xprocess.getinfo(Starter.name)
    info.terminate()

def test_records_cleanup_workflow(start_app):
    # 1. Create Stale Processed Record
    resp1 = requests.post(f"{BASE_URL}/records", json={
        "data": "test-processed",
        "status": "processed",
        "updated_at": "2020-01-01T00:00:00Z"
    })
    assert resp1.status_code == 200, f"Failed to create stale processed record. Status: {resp1.status_code}, Body: {resp1.text}"
    assert "id" in resp1.json(), "Response should contain 'id'"

    # 2. Create Recent Processed Record
    resp2 = requests.post(f"{BASE_URL}/records", json={
        "data": "test-recent-processed",
        "status": "processed",
        "updated_at": "2099-01-01T00:00:00Z"
    })
    assert resp2.status_code == 200, f"Failed to create recent processed record. Status: {resp2.status_code}, Body: {resp2.text}"

    # 3. Create Stale Failed Record
    resp3 = requests.post(f"{BASE_URL}/records", json={
        "data": "test-failed",
        "status": "failed",
        "updated_at": "2020-01-01T00:00:00Z"
    })
    assert resp3.status_code == 200, f"Failed to create stale failed record. Status: {resp3.status_code}, Body: {resp3.text}"

    # 4. Create Recent Failed Record
    resp4 = requests.post(f"{BASE_URL}/records", json={
        "data": "test-recent-failed",
        "status": "failed",
        "updated_at": "2099-01-01T00:00:00Z"
    })
    assert resp4.status_code == 200, f"Failed to create recent failed record. Status: {resp4.status_code}, Body: {resp4.text}"

    # 5. Run Cleanup Endpoint
    cleanup_resp = requests.post(f"{BASE_URL}/records/cleanup")
    assert cleanup_resp.status_code == 200, f"Cleanup endpoint failed. Status: {cleanup_resp.status_code}, Body: {cleanup_resp.text}"
    
    cleanup_data = cleanup_resp.json()
    assert "deleted_count" in cleanup_data, "Cleanup response should contain 'deleted_count'"
    assert cleanup_data["deleted_count"] == 2, f"Expected 2 records to be deleted, got {cleanup_data['deleted_count']}"

def test_cron_job_definition():
    # 6. Verify Cron Job Definition
    result = subprocess.run(
        ["grep", "-r", "cleanup-stale-records", PROJECT_DIR],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"Could not find cron job definition 'cleanup-stale-records' in {PROJECT_DIR}"
    assert "cleanup-stale-records" in result.stdout, "The output should contain the cron job definition."

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_index():
    r = client.get("/")
    assert r.status_code == 200


def test_task_endpoint():
    payload = {"area_id":"AREA_1", "date":"2023-01-01"}
    r = client.post("/api/task", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "done" or data["status"] == "queued"

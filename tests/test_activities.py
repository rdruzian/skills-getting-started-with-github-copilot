from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities():
    res = client.get("/activities")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, dict)
    # basic structure checks for a known activity
    assert "Chess Club" in data
    details = data["Chess Club"]
    assert "description" in details
    assert "participants" in details
    assert "max_participants" in details

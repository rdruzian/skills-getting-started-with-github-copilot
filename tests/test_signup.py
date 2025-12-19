from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)


def test_signup_success_and_duplicate():
    activity = "Chess Club"
    email = "fastapi_test@example.com"

    # Ensure clean starting state
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    # Successful signup
    res = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert res.status_code == 200
    assert email in activities[activity]["participants"]
    assert "Signed up" in res.json().get("message", "")

    # Duplicate signup should return 400
    res = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert res.status_code == 400
    assert res.json().get("detail") == "Already signed up for this activity"

    # Cleanup
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

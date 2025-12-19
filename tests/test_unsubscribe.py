from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)


def test_signup_and_unregister_flow():
    activity = "Math Club"
    email = "testuser@example.com"

    # Ensure clean state
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    # Sign up the test user
    res = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert res.status_code == 200
    assert email in activities[activity]["participants"]

    # Unregister the test user
    res = client.delete(f"/activities/{activity}/unregister", params={"email": email})
    assert res.status_code == 200
    assert email not in activities[activity]["participants"]
    assert "Unregistered" in res.json().get("message", "")


def test_unregister_nonexistent_returns_400():
    activity = "Math Club"
    email = "nonexistent@example.com"

    # Make sure the email is not registered
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    res = client.delete(f"/activities/{activity}/unregister", params={"email": email})
    assert res.status_code == 400
    assert res.json().get("detail") == "Email not registered for this activity"
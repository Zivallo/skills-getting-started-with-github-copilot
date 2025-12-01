from fastapi.testclient import TestClient
import uuid

from src import app as _app


client = TestClient(_app.app)


def test_get_activities_returns_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    # basic structure checks
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]


def test_signup_and_unregister_flow():
    activity = "Chess Club"
    # create a unique test email
    email = f"test+{uuid.uuid4().hex}@example.com"

    # sign up
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert resp.status_code == 200
    json_data = resp.json()
    assert "Signed up" in json_data.get("message", "")

    # verify email appears in participants
    resp = client.get("/activities")
    assert resp.status_code == 200
    activities = resp.json()
    participants = activities[activity]["participants"]
    assert email in participants

    # unregister the email
    resp = client.delete(f"/activities/{activity}/unregister", params={"email": email})
    assert resp.status_code == 200
    json_data = resp.json()
    assert "Unregistered" in json_data.get("message", "")

    # verify email no longer present
    resp = client.get("/activities")
    activities = resp.json()
    participants = activities[activity]["participants"]
    assert email not in participants

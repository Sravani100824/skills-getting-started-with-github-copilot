from copy import deepcopy

import pytest

from src.app import activities, app
from fastapi.testclient import TestClient

client = TestClient(app)


@pytest.fixture(autouse=True)

def reset_activities():
    original_activities = deepcopy(activities)
    yield
    activities.clear()
    activities.update(original_activities)

def test_signup_for_activity_no_email():
    activity_name = "Chess Club"
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": ""},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Email is required"


def test_signup_for_activity_already_signed_up():
    activity_name = "Programming Class"
    email = "emma@mergington.edu"
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == f"Student already signed up for {activity_name}"

def test_signup_for_activity_activity_not_found():
    activity_name = "some_random_activity"
    email = "somerandomemail@example.com"
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
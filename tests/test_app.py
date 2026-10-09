from fastapi.testclient import TestClient

from src.app import activities, app


client = TestClient(app)


def test_student_cannot_sign_up_for_activity_twice():
    activity = activities["Chess Club"]
    original_participants = activity["participants"].copy()
    email = "test-student@mergington.edu"

    try:
        first_response = client.post(
            "/activities/Chess Club/signup", params={"email": email}
        )
        second_response = client.post(
            "/activities/Chess Club/signup", params={"email": email}
        )

        assert first_response.status_code == 200
        assert second_response.status_code == 400
        assert second_response.json() == {"detail": "Student is already signed up"}
        assert activity["participants"].count(email) == 1
    finally:
        activity["participants"][:] = original_participants

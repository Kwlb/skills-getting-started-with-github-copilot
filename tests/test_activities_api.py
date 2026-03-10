def test_root_redirects_to_static_index(client):
    # Arrange
    expected_location = "/static/index.html"

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code in (302, 307)
    assert response.headers["location"] == expected_location


def test_get_activities_returns_activity_map(client):
    # Arrange
    required_keys = {"description", "schedule", "max_participants", "participants"}

    # Act
    response = client.get("/activities")
    payload = response.json()

    # Assert
    assert response.status_code == 200
    assert isinstance(payload, dict)
    assert "Programming Class" in payload
    assert required_keys.issubset(payload["Programming Class"].keys())
    assert isinstance(payload["Programming Class"]["participants"], list)


def test_signup_successfully_adds_participant(client):
    # Arrange
    activity_name = "Programming Class"
    student_email = "new.student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": student_email})
    activities_response = client.get("/activities")
    participants = activities_response.json()[activity_name]["participants"]

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {student_email} for {activity_name}"
    assert student_email in participants


def test_signup_unknown_activity_returns_404(client):
    # Arrange
    missing_activity = "Unknown Activity"
    student_email = "student@mergington.edu"

    # Act
    response = client.post(f"/activities/{missing_activity}/signup", params={"email": student_email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_duplicate_participant_returns_400(client):
    # Arrange
    activity_name = "Programming Class"
    existing_email = "emma@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": existing_email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_unregister_successfully_removes_participant(client):
    # Arrange
    activity_name = "Gym Class"
    existing_email = "john@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": existing_email},
    )
    activities_response = client.get("/activities")
    participants = activities_response.json()[activity_name]["participants"]

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {existing_email} from {activity_name}"
    assert existing_email not in participants


def test_unregister_unknown_activity_returns_404(client):
    # Arrange
    missing_activity = "Unknown Activity"
    student_email = "student@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{missing_activity}/participants",
        params={"email": student_email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_missing_participant_returns_404(client):
    # Arrange
    activity_name = "Gym Class"
    missing_email = "not.enrolled@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": missing_email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"
from src.app import activities


def test_root_redirects_to_index(client):
    # Arrange
    expected_location = "/static/index.html"

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == expected_location


def test_get_activities_returns_all_activities(client):
    # Arrange
    expected_activity = "Chess Club"

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    json_data = response.json()
    assert expected_activity in json_data
    assert "description" in json_data[expected_activity]
    assert isinstance(json_data[expected_activity]["participants"], list)


def test_signup_for_activity_adds_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    encoded_path = "/activities/Chess%20Club/signup"

    # Act
    response = client.post(encoded_path, params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}

    follow_up = client.get("/activities")
    assert email in follow_up.json()[activity_name]["participants"]


def test_signup_duplicate_participant_returns_400(client):
    # Arrange
    encoded_path = "/activities/Chess%20Club/signup"
    existing_email = "michael@mergington.edu"

    # Act
    response = client.post(encoded_path, params={"email": existing_email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"


def test_signup_to_missing_activity_returns_404(client):
    # Arrange
    encoded_path = "/activities/Band%20Club/signup"
    email = "student@mergington.edu"

    # Act
    response = client.post(encoded_path, params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_remove_participant_from_activity(client):
    # Arrange
    activity_name = "Programming Class"
    email = "emma@mergington.edu"
    encoded_path = "/activities/Programming%20Class/participants"

    # Act
    response = client.delete(encoded_path, params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Removed {email} from {activity_name}"}

    follow_up = client.get("/activities")
    assert email not in follow_up.json()[activity_name]["participants"]


def test_remove_missing_participant_returns_404(client):
    # Arrange
    encoded_path = "/activities/Programming%20Class/participants"
    email = "notfound@mergington.edu"

    # Act
    response = client.delete(encoded_path, params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"


def test_remove_participant_from_missing_activity_returns_404(client):
    # Arrange
    encoded_path = "/activities/Band%20Club/participants"
    email = "student@mergington.edu"

    # Act
    response = client.delete(encoded_path, params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"

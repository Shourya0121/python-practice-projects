def create_user_and_token(client, username, email):
    """Register a user and get an access token."""

    client.post(
        "/auth/register",
        json={
            "username" : username,
            "email" : email,
            "password" : "testpassword123",
        },
    )

    response = client.post(
        "/auth/login",
        data={
            "username" : username,
            "password" : "testpassword123",
        },
    )

    assert response.status_code == 200

    return response.json()["access_token"]

def test_create_task(client):
    token = create_user_and_token(
        client, "taskuser", "taskuser@example.com"
    )

    response = client.post(
        "/tasks/",
        json={
            "title": "Learn Pytest",
            "description": "Write an automated test",
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == "Learn Pytest"
    assert data["description"] == "Write an automated test"
    assert data["is_completed"] is False
    assert "owner_id" in data

def test_get_my_tasks(client):
    token = create_user_and_token(
        client, "listuser", "listuser@example.com"
    )

    headers = {"Authorization": f"Bearer {token}"}

    client.post(
        "/tasks/",
        json={"title": "First Task"},
        headers=headers,
    )

    client.post(
        "/tasks/",
        json={"title": "Second Task"},
        headers=headers,
    )

    response = client.get("/tasks/", headers=headers)

    assert response.status_code == 200
    assert len(response.json()) == 2

def test_get_single_task(client):
    token = create_user_and_token(
        client, "singleuser", "singleuser@example.com"
    )

    headers = {"Authorization": f"Bearer {token}"}

    create_response = client.post(
        "/tasks/",
        json={"title": "My task"},
        headers=headers,
    )

    task_id = create_response.json()["id"]

    response = client.get(
        f"/tasks/{task_id}",
        headers=headers,
    )

    assert response.status_code == 200
    assert response.json()["title"] == "My task"

    print("GET SINGLE TASK:", response.status_code, response.text)

def test_update_task(client):
    token = create_user_and_token(
        client, "updateuser", "updateuser@example.com"
    )

    headers = {"Authorization": f"Bearer {token}"}

    create_response = client.post(
        "/tasks/",
        json={"title": "Old title"},
        headers=headers,
    )

    task_id = create_response.json()["id"]

    response = client.patch(
        f"/tasks/{task_id}",
        json={
            "title": "Updated title",
            "is_completed": True,
        },
        headers=headers,
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Updated title"
    assert response.json()["is_completed"] is True


def test_delete_task(client):
    token = create_user_and_token(
        client, "deleteuser", "deleteuser@example.com"
    )

    headers = {"Authorization": f"Bearer {token}"}

    create_response = client.post(
        "/tasks/",
        json={"title": "Task to delete"},
        headers=headers,
    )

    task_id = create_response.json()["id"]


    response = client.delete(
        f"/tasks/{task_id}",
        headers=headers,
    )

    assert response.status_code == 204

    get_response = client.get(
        f"/tasks/{task_id}",
        headers=headers,
    )

    assert get_response.status_code == 404

def test_user_cannot_access_another_users_task(client):
    token1 = create_user_and_token(
        client, "owneruser", "owner@example.com"
    )

    headers1 = {"Authorization": f"Bearer {token1}"}


    create_response = client.post(
        "/tasks/",
        json={"title": "Private task"},
        headers=headers1,
    )

    task_id = create_response.json()["id"]

    token2 = create_user_and_token(
        client, "otheruser", "other@example.com"
    )

    headers2 = {"Authorization": f"Bearer {token2}"}

    response = client.get(
        f"/tasks/{task_id}",
        headers=headers2
    )

    assert response.status_code == 404

def test_access_tasks_without_token(client):
    response = client.get("/tasks/")

    assert response.status_code == 403

    print("UNAUTHORIZED RESPONSE:", response.status_code, response.text)
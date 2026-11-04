def test_register_user(client):
    response = client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpassword123",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["username"] == "testuser"
    assert data["email"] == "testuser@example.com"
    assert "password" not in data
    assert "hashed_password" not in data

def test_register_duplicate_user(client):
    user_data = {
        "username" : "duplicateuser",
        "email" : "duplicate@example.com",
        "password" : "testpassword123",
    }

    first_response = client.post("/auth/register", json=user_data)
    second_response = client.post("/auth/register", json=user_data)

    assert first_response.status_code == 201
    assert second_response.status_code == 409


def test_login_success(client):
    client.post(
        "/auth/register",
        json={
            "username" : "loginuser",
            "email" : "login@example.com",
            "password" : "testpassword123",
        },
    )

    response = client.post(
        "/auth/login",
        data={
            "username" : "loginuser",
            "password" : "testpassword123",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"].lower() == "bearer"

def test_login_wrong_password(client):
    client.post(
        "/auth/register",
        json={
            "username" : "wrongpassuser",
            "email" : "wrongpass@example.com",
            "password" : "testpassword123",
        },
    )

    response = client.post(
        "/auth/login",
        data={
            "username" : "wrongpassuser",
            "password" : "wrongpassword",
        },
    )

    assert response.status_code == 401


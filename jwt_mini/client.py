import requests

BASE_URL = "http://127.0.0.1:8000"

access_token = None
refresh_token = None

def login():
    global access_token, refresh_token

    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={
        "username": "john",
        "password": "john123"
    }
    )

    print("login status:", response.status_code)
    print("login response:", response.json())

    if response.status_code != 200:
        return

    data = response.json()

    access_token = data["access_token"]
    refresh_token = data["refresh_token"]

    print("Login Successful")
    print("Access token received")
    print("Refresh token received")


def refresh_access_token():
    global access_token

    response = requests.post(
        f"{BASE_URL}/auth/refresh",
        json={
            "refresh_token": refresh_token
        }
    )

    print("refresh status:", response.status_code)
    print("refresh response:", response.json())

    if response.status_code !=200:
        print("refresh failed")
        return False

    data = response.json()

    access_token = data["access_token"]

    print("New Access token Received")

    return True

def get_current_user():
    response = requests.get(
        f"{BASE_URL}/users/me",
        headers={
                "Authorization": f"Bearer {access_token}"
        }
    )

    print("user request status:", response.status_code)
    print(response.json())

login()
get_current_user()
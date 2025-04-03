import pytest

@pytest.mark.auth
def test_register_user(client):
    response = client.post(
        "/signup",
        json={"email": "testuser@example.com", "username": "testuser", "password": "testpassword"}
    )
    assert response.status_code == 200
    assert response.json()["email"] == "testuser@example.com"

@pytest.mark.auth
def test_register_user_duplicate(client):
    client.post("/signup", json={"email": "duplicate@example.com", "username": "dupuser", "password": "testpass"})
    response = client.post("/signup", json={"email": "duplicate@example.com", "username": "dupuser", "password": "testpass"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

@pytest.mark.auth
def test_login_user(client):
    client.post("/signup", json={"email": "login@example.com", "username": "loginuser", "password": "password123"})
    response = client.post("/login", data={"username": "login@example.com", "password": "password123"})
    
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()

@pytest.mark.auth
def test_refresh_token(client):
    client.post("/signup", json={"email": "refresh@example.com", "username": "refreshuser", "password": "securepass"})
    login_response = client.post("/login", data={"username": "refresh@example.com", "password": "securepass"})
    refresh_token = login_response.json()["refresh_token"]

    refresh_response = client.post("/refresh", json={"refresh_token": refresh_token})
    
    assert refresh_response.status_code == 200
    assert "access_token" in refresh_response.json()

@pytest.mark.auth
def test_logout(client):
    response = client.post("/logout")
    assert response.status_code == 200
    assert response.json()["message"] == "Successfully logged out"

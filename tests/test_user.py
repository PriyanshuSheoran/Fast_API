import pytest

@pytest.mark.user
def test_get_user_profile(client, authenticated_user):
    """Test retrieving the current user profile."""
    response = client.get("/users/me", headers=authenticated_user)
    
    assert response.status_code == 200
    assert "email" in response.json()
    assert "username" in response.json()

@pytest.mark.user
def test_update_user_username(client, authenticated_user):
    """Test updating the username of the current user."""
    response = client.put(
        "/users/me",
        json={"username": "new_username"},
        headers=authenticated_user
    )
    
    assert response.status_code == 200
    assert response.json()["username"] == "new_username"

@pytest.mark.user
def test_update_user_email(client, authenticated_user):
    """Test updating the email of the current user."""
    response = client.put(
        "/users/me",
        json={"email": "new_email@example.com"},
        headers=authenticated_user
    )
    
    assert response.status_code == 200
    assert response.json()["email"] == "new_email@example.com"

@pytest.mark.user
def test_update_user_password(client, authenticated_user):
    """Test updating the password of the current user."""
    response = client.put(
        "/users/me",
        json={"password": "newsecurepassword"},
        headers=authenticated_user
    )
    
    assert response.status_code == 200
    assert "email" in response.json() 

@pytest.mark.user
def test_update_user_invalid(client, authenticated_user):
    """Test updating a user with invalid data."""
    response = client.put(
        "/users/me",
        json={"email": "not-an-email"},
        headers=authenticated_user
    )
    
    assert response.status_code == 422  

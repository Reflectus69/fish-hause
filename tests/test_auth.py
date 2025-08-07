import pytest
from fastapi.testclient import TestClient

def test_register_user(client: TestClient):
    """
    Test user registration endpoint.
    """
    response = client.post(
        "/api/v1/auth/register",
        json={"email": "test@example.com", "password": "password123", "name": "Test User"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data
    assert "hashed_password" not in data # Ensure password is not returned

def test_login_for_access_token(client: TestClient):
    """
    Test login endpoint after registering a user.
    """
    # First, register a user
    client.post(
        "/api/v1/auth/register",
        json={"email": "testlogin@example.com", "password": "password123", "name": "Test Login User"},
    )

    # Now, try to log in
    response = client.post(
        "/api/v1/auth/token",
        data={"username": "testlogin@example.com", "password": "password123"},
        headers={"content-type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

import os
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Test health check

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

# Test user registration and login

def test_register_and_login():
    # Register a new user
    user_data = {
        "username": "pytestuser",
        "email": "pytestuser@example.com",
        "password": "pytestpass"
    }
    response = client.post("/auth/register", json=user_data)
    assert response.status_code in (200, 400)  # 400 if already exists

    # Login
    login_data = {
        "username": "pytestuser",
        "password": "pytestpass"
    }
    response = client.post("/auth/login", data=login_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["user"]["username"] == "pytestuser"
    token = data["access_token"]
    return token

# Test get users (requires auth)

def test_get_users():
    token = test_register_and_login()
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/users/", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# Test get licenses (public)
def test_get_licenses():
    response = client.get("/licenses/")
    assert response.status_code == 200
    assert isinstance(response.json(), list) 
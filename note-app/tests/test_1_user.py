# import io
# from test_note_crud import client
import pytest
from main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_user_registration():
    response = client.post(
        "/auth/register/",
        json={
            "username": "testuser",
            "email": "test@test.com",
            "password": "password",
        }
    )
    assert response.status_code == 201
    # assert response.json()["username"] == "testuser"
    # assert response.json()["email"] == "test@test.com"

def test_user_login():
    response = client.post(
        "/auth/token/",
        data={
            "username": "testname",
            "password": "password"
        }
    )
    assert response.status_code == 200

def get_token():
    response = client.post(
        "/auth/token/",
        data={
            "username": "testuser",
            "password": "password"
        }
    )
    return response.json()["access_token"]
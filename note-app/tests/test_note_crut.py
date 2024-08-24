from main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def return_note():
    return {
        "title": "Test title",
        "content": "Test content",
        "user_id": 1,
        "image": [
            {
                "url": "images/image.jpg"
            }
        ]
    }

def test_create_note():
    response = client.post(
        "/note/create",
        json=return_note
    )
    assert response.status_code == 201
    assert response.json() == return_note

def test_get_note():
    response = client.get("/note/1")
    assert response.status_code == 200
    assert response.json() == return_note

def test_update_note():
    response = client.put(
        "/note/update/1",
        json=return_note
    )
    assert response.status_code == 200
    assert response.json() == return_note
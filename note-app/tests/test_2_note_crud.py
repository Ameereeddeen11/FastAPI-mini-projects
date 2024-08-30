import io, pytest
from main import app
from fastapi.testclient import TestClient
from .test_1_user import get_token

client = TestClient(app)

datas = {
    "title": "Test Note",
    "content": "This is a test note"
}

update_datas = {
    "title": "Updated Note",
    "content": "This is an updated note"
}

files = {
    "files": (
        "test.jpg",
        io.BytesIO(b"some binary data"),
        "image/jpeg"
    )
}

def test_create_note():
    create_note = client.post(
        "/note/create/",
        headers={"Authorization": f"bearer {get_token()}"},
        data=datas,
        files=files
    )
    assert create_note.status_code == 201

def test_get_note():
    response = client.get(
        "/note/1/",
        headers={"Authorization": f"bearer {get_token()}"}
    )
    assert response.status_code == 200
    # assert response.json() == datas

def test_update_note():
    response = client.put(
        "/note/update/1/",
        headers={"Authorization": f"bearer {get_token()}"},
        json=update_datas
    )
    assert response.status_code == 200

def test_delete_note():
    response = client.delete(
        "/note/delete/1/",
        headers={"Authorization": f"bearer {get_token()}"}
    )
    assert response.status_code == 200
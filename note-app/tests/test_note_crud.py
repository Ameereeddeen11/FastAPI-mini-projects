import io, pytest
from main import app
from fastapi.testclient import TestClient
from .test_user import test_user_login

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

@pytest.mark.order(1)
def test_create_note():
    response = client.post(
        "/auth/token/",
        data={
            "username": "testname",
            "password": "password"
        }
    )
    token = response.json()["access_token"]
    create_note = client.post(
        "/note/create",
        headers={"Authorization": f"bearer {token}"},
        data=datas,
        files=files
    )
    assert create_note.status_code == 201
    assert create_note.json()["title"] == datas["title"]
    assert create_note.json()["content"] == datas["content"]

@pytest.mark.order(2)
def test_get_note():
    response = client.post(
        "/auth/token/",
        data={
            "username": "testname",
            "password": "password"
        }
    )
    token = response.json()["access_token"]
    response = client.get(
        "/note/1",
        headers={"Authorization": f"bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json() == datas

@pytest.mark.order(3)
def test_update_note():
    response = client.post(
        "/auth/token/",
        data={
            "username": "testname",
            "password": "password"
        }
    )
    token = response.json()["access_token"]
    response = client.put(
        "/note/update/1",
        headers={"Authorization": f"bearer {token}"},
        json=update_datas
    )
    assert response.status_code == 200
    assert response.json() == update_datas
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_get_all_blogs():
    response = client.get('/blog/all')
    assert response.status_code == 200


def test_auth_error():
    response = client.post('/token',
                           data={"username": "", "password": ""})
    access_token = response.json().get('access_token')

    assert access_token is None
    message = response.json().get('detail')[0].get('msg')
    assert message == "field required"


def test_auth_success():
    response = client.post('/token',
                           data={"username": "Nick", "password": "Nick"})
    access_token = response.json().get('access_token')

    assert access_token


# FIXME: сделать удаление из базы после создания тестовых данных
def test_post_article():
    auth = client.post('/token',
                           data={"username": "Nick", "password": "Nick"})
    access_token = auth.json().get('access_token')

    assert access_token

    response = client.post('/article/create',
                           json={
                               "title": "Test article",
                               "content": "test content",
                               "published": True,
                               "creator_id": 8
                           },
                           headers={"Authorization": "bearer " + access_token})

    assert response.status_code == 201
    assert response.json().get("title") == "Test article"

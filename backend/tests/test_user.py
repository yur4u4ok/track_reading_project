import pytest

from rest_framework.test import APIClient

client = APIClient()


@pytest.mark.django_db
def test_register_user():
    payload = dict(
        email='user@gmail.com',
        password='user',
        profile=dict(
            name="Ostap",
            surname="Yurchuk"
        )
    )

    response = client.post("/auth/register", payload, format='json')

    data = response.data

    assert data["email"] == payload["email"]
    assert "password" not in data
    assert data['profile']['name'] == payload['profile']['name']


@pytest.mark.django_db
def test_login_user():
    payload = dict(
        email='user@gmail.com',
        password='user',
        profile=dict(
            name="Ostap",
            surname="Yurchuk"
        )
    )

    client.post('/auth/register', payload, format='json')

    response = client.post('/auth', dict(email='user@gmail.com', password='user'))

    assert response.status_code == 200


@pytest.mark.django_db
def test_login_user_fail():
    response = client.post('/auth', dict(email='user@gmail.com', password='user'))

    assert response.status_code == 401

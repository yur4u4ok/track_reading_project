import pytest

from rest_framework.test import APIClient

client = APIClient()


@pytest.mark.django_db
def test_create_book():
    payload = dict(
        name='American dreamer',
        author='Tommy Hilfiger',
        year=2020,
        short_description='about business',
        full_description='How Tommy created one of the biggest companies'
    )

    response_post = client.post('/books', payload)
    response_get = client.get('/books')

    data = response_get.data

    assert response_post.status_code == 201
    assert len(data) == 1


@pytest.mark.django_db
def test_get_book():
    payload = dict(
        name='American dreamer',
        author='Tommy Hilfiger',
        year=2020,
        short_description='about business',
        full_description='How Tommy created one of the biggest companies'
    )

    client.post('/books', payload)
    response = client.get('/books')

    data = response.data

    assert data[0]['short_description'] == 'about business'


@pytest.mark.django_db
def test_start_end_session():
    user_payload = dict(
        email='user@gmail.com',
        password='user',
        profile=dict(
            name="Ostap",
            surname="Yurchuk"
        )
    )

    book_payload = dict(
        name='American dreamer',
        author='Tommy Hilfiger',
        year=2020,
        short_description='about business',
        full_description='How Tommy created one of the biggest companies'
    )

    book_create_response = client.post('/books', book_payload)
    client.post('/auth/register', user_payload, format='json')
    login_response = client.post('/auth', dict(email='user@gmail.com', password='user'))

    access_token = login_response.data['access']
    book_id = book_create_response.data['id']

    start_session_response = client.post(f'/books/{book_id}/start_session', headers={
        "Authorization": f'Bearer {access_token}'
    })

    end_session_response = client.patch(f'/books/{book_id}/end_session', headers={
        "Authorization": f'Bearer {access_token}'
    })

    assert start_session_response.status_code == 201
    assert end_session_response.status_code == 200
    assert end_session_response.data['start_reading'] == start_session_response.data['start_reading']


@pytest.mark.django_db
def test_every_book_time_fail():
    response = client.post('/books/every_book_time')

    assert response.status_code == 401


@pytest.mark.django_db
def test_general_time():
    user_payload = dict(
        email='user@gmail.com',
        password='user',
        profile=dict(
            name="Ostap",
            surname="Yurchuk"
        )
    )

    client.post('/auth/register', user_payload, format='json')
    login_response = client.post('/auth', dict(email='user@gmail.com', password='user'))

    access_token = login_response.data['access']

    general_time_response = client.get('/books/general_time', headers={
        "Authorization": f'Bearer {access_token}'
    })

    assert type(general_time_response.data['general_time_reading']) == str

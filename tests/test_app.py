from http import HTTPStatus

import pytest

from fast_api_dunossauro.schemas import UserPublic


def test_root_must_return_ok_and_hello_world(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Hello, World!'}


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'testusername',
            'email': 'test@test.com',
            'password': 'testpassword',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'username': 'testusername',
        'email': 'test@test.com',
    }


def test_create_user_with_duplicate_username_returns_bad_request(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.post(
        '/users/',
        json={
            'username': user_schema['username'],
            'email': 'another@mail.com',
            'password': 'str0ngpass',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Username already exists.'}


def test_create_user_with_duplicate_email_returns_bad_request(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.post(
        '/users/',
        json={
            'username': 'anotherusername',
            'email': user_schema['email'],
            'password': 'str0ngpass',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Email already exists.'}


def test_get_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_get_user_with_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')
    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'newusername',
            'email': 'oto@email.com',
            'password': 'newpassword',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'newusername',
        'email': 'oto@email.com',
    }


@pytest.mark.skip(reason='The token prevents this behavior')
def test_update_user_not_found(client, token):
    response = client.put(
        '/users/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'newusername',
            'email': 'test@test.com',
            'password': 'newpassword',
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_update_integrity_error(client, user, token):
    client.post(
        '/users',
        json={
            'username': 'fausto',
            'email': 'fausto@silva.com',
            'password': 'ohlocobixo',
        },
    )

    response_update = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'fausto',
            'email': 'test@test.com',
            'password': 'ohlocobixo',
        },
    )

    assert response_update.status_code == HTTPStatus.CONFLICT
    assert response_update.json() == {
        'detail': 'Username or email already exists.'
    }


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


@pytest.mark.skip(reason='The token prevents this behavior')
def test_delete_user_not_found(client):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_token(client, user):
    response = client.post(
        '/token',
        data={
            'username': user.email,
            'password': user.clean_password,
        },
    )

    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert token['token_type'] == 'Bearer'
    assert 'access_token' in token


def test_token_invalid_credentials(client, user):
    response = client.post(
        '/token',
        data={'username': user.email, 'password': 'invalid'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect email or password'}

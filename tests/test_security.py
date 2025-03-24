from http import HTTPStatus

from jwt import decode

from fast_api_dunossauro.security import create_access_token
from fast_api_dunossauro.settings import Settings

settings = Settings()


def test_jwt_creation():
    data = {'sub': 'test@test.com'}

    result = create_access_token(data)

    decoded_result = decode(
        result,
        settings.SECRET_KEY,
        algorithms=[settings.ALGORITHM],
    )

    assert decoded_result['sub'] == data['sub']
    assert decoded_result['exp'] is not None


def test_jwt_invalid_token(client):
    response = client.delete(
        '/users/1',
        headers={'Authorization': 'Bearer invalid_token'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}

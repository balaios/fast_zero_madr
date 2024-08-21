from http import HTTPStatus

import pytest
from fastapi import HTTPException
from jwt import decode

from fast_zero_madr.security import (
    create_access_token,
    get_current_user,
    settings,
)


def test_jwt():
    data = {'test': 'test'}
    token = create_access_token(data)

    decoded = decode(
        token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
    )

    assert decoded['test'] == data['test']
    assert decoded['exp']


def test_jwt_invalid_token(client):
    response = client.delete(
        '/user/1', headers={'Authorization': 'Bearer token-invalido'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {
        'detail': 'Não foi possível validar as credenciais'
    }


def test_get_current_not_user():
    data = {}
    token = create_access_token(data)

    with pytest.raises(HTTPException):
        get_current_user(token=token)


def test_get_current_user_invalid(session):
    data = {'sub': 'test@test.com'}
    token = create_access_token(data)

    with pytest.raises(HTTPException):
        get_current_user(session=session, token=token)

from http import HTTPStatus

from freezegun import freeze_time


def test_login_for_access_token_ok(client, user):
    response = client.post(
        '/auth/token/',
        data={'username': user.email, 'password': user.clean_password},
    )
    token_data = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token_data
    assert 'token_type' in token_data


def test_login_for_access_token_wrong_email(client, user):
    response = client.post(
        '/auth/token/',
        data={'username': 'wrong@email.com', 'password': user.clean_password},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Email ou senha incorretos'}


def test_login_for_access_token_wrong_password(client, user):
    response = client.post(
        '/auth/token/',
        data={'username': user.email, 'password': 'wrong_password'},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Email ou senha incorretos'}


def test_refresh_token_ok(client, user, token):
    response = client.post(
        '/auth/refresh_token/',
        headers={'Authorization': f'Bearer {token}'},
    )

    data = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in data
    assert 'token_type' in data
    assert data['token_type'] == 'bearer'


def test_refresh_access_token_expired(client, user):
    with freeze_time('2023-07-14 12:00:00'):
        response = client.post(
            '/auth/token',
            data={'username': user.email, 'password': user.clean_password},
        )
        assert response.status_code == HTTPStatus.OK
        token_data = response.json()['access_token']

    with freeze_time('2023-07-14 13:31:00'):
        response = client.post(
            '/auth/refresh_token',
            headers={'Authorization': f'Bearer {token_data}'},
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {
            'detail': 'Não foi possível validar as credenciais'
        }


# TODO: fix
# def test_token_expired_after_time(client, user):
#     with freeze_time('2023-07-14 12:00:00'):
#         response = client.post(
#             '/auth/token',
#             data={'username': user.email, 'password': user.clean_password},
#         )
#         assert response.status_code == HTTPStatus.OK
#         token_data = response.json()['access_token']
#
#     with freeze_time('2023-07-14 13:01:00'):
#         response = client.put(
#             f'/user/{user.id}',
#             headers={'Authorization': f'Bearer {token_data}'},
#             json={
#                 'username': 'wrongwrong',
#                 'email': 'wrong@wrong.com',
#                 'password': 'wrong',
#             },
#         )
#         assert response.status_code == HTTPStatus.UNAUTHORIZED
#         assert response.json() == {
#             'detail': 'Não foi possível validar as credenciais'
#         }

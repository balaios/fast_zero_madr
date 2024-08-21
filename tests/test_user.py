from http import HTTPStatus


def test_create_user_ok(client):
    response = client.post(
        '/user/',
        json={
            'username': 'alice',
            'email': 'alice@example.com',
            'senha': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'alice',
        'email': 'alice@example.com',
        'id': 1,
    }


def test_create_user_username_already_exists(client, user):
    response = client.post(
        '/user/',
        json={
            'username': user.username,
            'email': 'alice@example.com',
            'senha': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Conta já cadastrada'}


def test_create_user_email_already_exists(client, user):
    response = client.post(
        '/user/',
        json={
            'username': 'alice',
            'email': user.email,
            'senha': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Email já cadastrado'}


def test_update_user_ok(client, user, token):
    response = client.put(
        f'/user/{user.id}/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'alice',
            'email': 'alice@example.com',
            'senha': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'alice',
        'email': 'alice@example.com',
        'id': user.id,
    }


def test_update_user_with_other_user(client, other_user, token):
    response = client.put(
        f'/user/{other_user.id}/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'alice',
            'email': 'alice@example.com',
            'senha': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Não autorizado'}


def test_delete_user_ok(client, user, token):
    response = client.delete(
        f'/user/{user.id}/', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Conta deletada com sucesso'}


def test_delete_user_other_user(client, other_user, token):
    response = client.delete(
        f'/user/{other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Não autorizado'}

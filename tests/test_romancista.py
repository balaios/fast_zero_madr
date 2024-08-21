from http import HTTPStatus

from tests.factories import RomancistaFactory


def test_create_romancista_ok(client, token):
    response = client.post(
        '/romancista/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'nome': 'Clarice Lispector',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'nome': 'Clarice Lispector',
    }


def test_create_romancista_already_exists(client, romancista, token):
    response = client.post(
        '/romancista/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'nome': romancista.nome,
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Romancista já cadastrado'}


def test_read_romancista_ok(client, romancista, token):
    response = client.get(
        f'/romancista/{romancista.id}/',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'id': romancista.id, 'nome': romancista.nome}


def test_read_romancista_does_not_exist(client, token):
    response = client.get(
        '/romancista/1/',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Romancista não consta no MADR'}


def test_read_filter_romancista(session, client, token):
    expected_romancista = 5
    session.bulk_save_objects(
        RomancistaFactory.create_batch(expected_romancista)
    )
    response = client.get(
        '/romancista/?nome=test',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['romancistas']) == expected_romancista


def test_update_romancista_ok(client, romancista, token):
    response = client.put(
        f'/romancista/{romancista.id}/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'nome': 'alice updated',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'nome': 'alice updated', 'id': romancista.id}


def test_update_romancista_already_exists(
    client, romancista, other_romancista, token
):
    response = client.put(
        f'/romancista/{romancista.id}/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'nome': other_romancista.nome,
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'romancista já consta no MADR'}


def test_update_romancista_does_not_exist(client, token):
    response = client.put(
        '/romancista/1/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'nome': 'alice updated',
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Romancista não consta no MADR'}


def test_delete_romancista_ok(client, romancista, token):
    response = client.delete(
        f'/romancista/{romancista.id}/',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'nome': romancista.nome, 'id': romancista.id}


def test_delete_romancista_does_not_exist(client, token):
    response = client.delete(
        '/romancista/1/',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Romancista não consta no MADR'}

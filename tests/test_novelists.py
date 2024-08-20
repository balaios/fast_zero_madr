from http import HTTPStatus

from tests.factories import NovelistFactory


def test_create_novelist(client, token):
    response = client.post(
        '/novelists/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'name': 'Clarice Lispector',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'name': 'Clarice Lispector',
    }


def test_create_novelist_already_exists(client, novelist, token):
    response = client.post(
        '/novelists/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'name': novelist.name,
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Romancista já cadastrado'}


def test_read_novelist(client, novelist, token):
    response = client.get(
        f'/novelists/{novelist.id}/',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'id': novelist.id, 'name': novelist.name}


def test_read_novelist_does_not_exist(client, token):
    response = client.get(
        '/novelists/1/',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Romancista não consta no MADR'}


def test_read_filter_novelists(session, client, token):
    expected_todos = 5
    session.bulk_save_objects(NovelistFactory.create_batch(expected_todos))
    response = client.get(
        '/novelists/?name=test',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['novelists']) == expected_todos


def test_update_novel(client, novelist, token):
    response = client.put(
        f'/novelists/{novelist.id}/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'name': 'alice updated',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'name': 'alice updated', 'id': novelist.id}


def test_update_novel_does_not_exist(client, token):
    response = client.put(
        '/novelists/1/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'name': 'alice updated',
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Romancista não consta no MADR'}


def test_delete_novelist(client, novelist, token):
    response = client.delete(
        f'/novelists/{novelist.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'name': novelist.name, 'id': novelist.id}


def test_delete_novelist_does_not_exist(client, token):
    response = client.delete(
        '/novelists/1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Romancista não consta no MADR'}

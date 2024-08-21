from http import HTTPStatus

from tests.factories import LivroFactory, RomancistaFactory


def test_create_livro_ok(client, romancista, token):
    response = client.post(
        '/livro/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'titulo': 'livro teste',
            'id_romancista': romancista.id,
            'ano': 2018,
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'titulo': 'livro teste',
        'id_romancista': romancista.id,
        'ano': 2018,
    }


def test_create_livro_already_exists(client, livro, token):
    response = client.post(
        '/livro/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'titulo': livro.titulo,
            'id_romancista': livro.id_romancista,
            'ano': livro.ano,
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Romancista já cadastrado'}


def test_read_livro_ok(client, livro, token):
    response = client.get(
        f'/livro/{livro.id}/',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': livro.id,
        'titulo': livro.titulo,
        'ano': livro.ano,
        'id_romancista': livro.id_romancista,
    }


def test_read_livro_does_not_exist(client, token):
    response = client.get(
        '/livro/1/',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Livro não consta no MADR'}


def test_read_filter_livro_titulo_ok(session, client, token):
    expected_todos = 5

    for _ in range(expected_todos):
        db_romancista = RomancistaFactory()
        session.add(db_romancista)
        session.commit()
        db_book = LivroFactory(id_romancista=db_romancista.id)
        session.add(db_book)
        session.commit()

    response = client.get(
        '/livro/?titulo=test',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['livros']) == expected_todos


def test_read_filter_livro_ano_ok(session, client, token):
    expected_todos = 5

    for _ in range(expected_todos):
        db_romancista = RomancistaFactory()
        session.add(db_romancista)
        session.commit()
        db_book = LivroFactory(id_romancista=db_romancista.id, ano=1989)
        session.add(db_book)
        session.commit()

    response = client.get(
        '/livro/?ano=1989',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['livros']) == expected_todos


def test_read_filter_livro_titulo_ano_ok(session, client, token):
    expected_todos = 5

    for _ in range(expected_todos):
        db_romancista = RomancistaFactory()
        session.add(db_romancista)
        session.commit()
        db_book = LivroFactory(id_romancista=db_romancista.id, ano=2024)
        session.add(db_book)
        session.commit()

    response = client.get(
        '/livro/?titulo=test&ano=2024',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['livros']) == expected_todos


def test_update_livro_ok(client, livro, token):
    response = client.put(
        f'/livro/{livro.id}/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'titulo': 'alice updated',
            'ano': livro.ano,
            'id_romancista': livro.id_romancista,
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'titulo': 'alice updated',
        'id': livro.id,
        'ano': livro.ano,
        'id_romancista': livro.id_romancista,
    }


def test_update_livro_other_livro(client, livro, other_livro, token):
    response = client.put(
        f'/livro/{livro.id}/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'titulo': other_livro.titulo,
            'ano': livro.ano,
            'id_romancista': livro.id_romancista,
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'livro já consta no MADR'}


def test_update_book_does_not_exist(client, token):
    response = client.put(
        '/livro/1/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'titulo': 'alice updated',
            'ano': 1920,
            'id_romancista': 1,
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'livro não consta no MADR'}


def test_delete_book(client, livro, token):
    response = client.delete(
        f'/livro/{livro.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'titulo': livro.titulo,
        'id': livro.id,
        'ano': livro.ano,
        'id_romancista': livro.id_romancista,
    }


def test_delete_book_does_not_exist(client, token):
    response = client.delete(
        '/livro/1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'livro não consta no MADR'}

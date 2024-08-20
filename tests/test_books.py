from http import HTTPStatus

from tests.factories import BookFactory, NovelistFactory


def test_create_book(client, novelist, token):
    response = client.post(
        '/books/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'title': 'livro teste',
            'novelist_id': novelist.id,
            'year': 2018,
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'title': 'livro teste',
        'novelist_id': novelist.id,
        'year': 2018,
    }


def test_create_book_already_exists(client, book, token):
    response = client.post(
        '/books/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'title': book.title,
            'novelist_id': book.novelist_id,
            'year': book.year,
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Romancista já cadastrado'}


def test_read_book(client, book, token):
    response = client.get(
        f'/books/{book.id}/',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': book.id,
        'title': book.title,
        'year': book.year,
        'novelist_id': book.novelist_id,
    }


def test_read_book_does_not_exist(client, token):
    response = client.get(
        '/books/1/',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Livro não consta no MADR'}


def test_read_filter_title_books(session, client, token):
    expected_todos = 5

    for _ in range(expected_todos):
        db_novelist = NovelistFactory()
        session.add(db_novelist)
        session.commit()
        db_book = BookFactory(novelist_id=db_novelist.id)
        session.add(db_book)
        session.commit()

    response = client.get(
        '/books/?title=test',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['books']) == expected_todos


def test_update_book(client, book, token):
    response = client.put(
        f'/books/{book.id}/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'title': 'alice updated',
            'year': book.year,
            'novelist_id': book.novelist_id,
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'title': 'alice updated',
        'id': book.id,
        'year': book.year,
        'novelist_id': book.novelist_id,
    }


def test_update_book_does_not_exist(client, token):
    response = client.put(
        '/books/1/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'title': 'alice updated',
            'year': 1920,
            'novelist_id': 1,
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Romancista não consta no MADR'}


def test_delete_book(client, book, token):
    response = client.delete(
        f'/books/{book.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'title': book.title,
        'id': book.id,
        'year': book.year,
        'novelist_id': book.novelist_id,
    }


def test_delete_book_does_not_exist(client, token):
    response = client.delete(
        '/books/1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Livro não consta no MADR'}

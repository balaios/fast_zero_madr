import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from testcontainers.postgres import PostgresContainer

from fast_zero_madr.app import app
from fast_zero_madr.database import get_session
from fast_zero_madr.models import table_registry
from fast_zero_madr.security import get_password_hash
from tests.factories import LivroFactory, RomancistaFactory, UserFactory


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture(scope='session')
def engine():
    with PostgresContainer('postgres:16', driver='psycopg') as postgres:
        _engine = create_engine(postgres.get_connection_url())

        with _engine.begin():
            yield _engine


@pytest.fixture
def session(engine):
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session
        session.rollback()

    table_registry.metadata.drop_all(engine)


@pytest.fixture
def user(session):
    password = 'testtest'
    user = UserFactory(senha=get_password_hash(password))

    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = 'testtest'

    return user


@pytest.fixture
def other_user(session):
    password = 'testtest'
    other_user = UserFactory(senha=get_password_hash(password))

    session.add(other_user)
    session.commit()
    session.refresh(other_user)

    other_user.clean_password = 'testtest'

    return other_user


@pytest.fixture
def romancista(session):
    romancista = RomancistaFactory()

    session.add(romancista)
    session.commit()
    session.refresh(romancista)

    return romancista


@pytest.fixture
def other_romancista(session):
    other_romancista = RomancistaFactory()

    session.add(other_romancista)
    session.commit()
    session.refresh(other_romancista)

    return other_romancista


@pytest.fixture
def livro(session, romancista):
    livro = LivroFactory(id_romancista=romancista.id)

    session.add(livro)
    session.commit()
    session.refresh(livro)

    return livro


@pytest.fixture
def other_livro(session, romancista):
    other_livro = LivroFactory(id_romancista=romancista.id)

    session.add(other_livro)
    session.commit()
    session.refresh(other_livro)

    return other_livro


@pytest.fixture
def token(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    return response.json()['access_token']

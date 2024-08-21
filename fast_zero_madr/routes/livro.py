from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero_madr.database import get_session
from fast_zero_madr.models import Livro, User
from fast_zero_madr.schemas import (
    LivroPublic,
    LivroPublicList,
    LivroSchema,
    Message,
)
from fast_zero_madr.security import get_current_user

router = APIRouter(prefix='/livro', tags=['livro'])


T_Session = Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post(
    '/',
    status_code=HTTPStatus.CREATED,
    response_model=LivroPublic,
    responses={
        409: {
            'model': Message,
            'description': 'Conflict',
            'example': {'detail': 'Romancista já cadastrado'},
        },
        500: {'model': Message, 'description': 'Internal Server Error'},
    },
)
def create_livro(livro: LivroSchema, session: T_Session, _: T_CurrentUser):
    db_livro = session.scalar(
        select(Livro).where(Livro.titulo == livro.titulo)
    )

    if db_livro:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Romancista já cadastrado',
        )

    db_livro = Livro(
        titulo=livro.titulo, ano=livro.ano, id_romancista=livro.id_romancista
    )

    session.add(db_livro)
    session.commit()
    session.refresh(db_livro)

    return db_livro


@router.get('/{livro_id}/', response_model=LivroPublic)
def read_livro(
    livro_id: int,
    session: T_Session,
    _: T_CurrentUser,
):
    db_livro = session.scalar(select(Livro).where(Livro.id == livro_id))

    if not db_livro:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Livro não consta no MADR',
        )
    return db_livro


@router.get('/', response_model=LivroPublicList)
def read_filter_livro(
    session: T_Session,
    _: T_CurrentUser,
    titulo: str = Query(None),
    ano: int = Query(None),
    offset: int = Query(None),
    limit: int = Query(None),
):
    query = select(Livro)

    if titulo:
        query = query.filter(Livro.titulo.contains(titulo))

    if ano:
        query = query.filter(Livro.ano == ano)

    db_livros = session.scalars(query.offset(offset).limit(limit)).all()

    return {'livros': db_livros}


@router.put('/{livro_id}/', response_model=LivroPublic)
def update_livro(
    livro_id: int,
    livro: LivroSchema,
    session: T_Session,
    _: T_CurrentUser,
):
    db_livro = session.scalar(select(Livro).where(Livro.id == livro_id))

    if not db_livro:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='livro não consta no MADR',
        )

    mew_titulo = session.scalar(
        select(Livro).where(Livro.titulo == livro.titulo)
    )

    if mew_titulo:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='livro já consta no MADR',
        )

    for key, value in livro.model_dump(exclude_unset=True).items():
        setattr(db_livro, key, value)

    session.commit()
    session.refresh(db_livro)

    return db_livro


@router.delete('/{livro_id}/', response_model=LivroPublic)
def delete_livro(
    livro_id: int,
    session: T_Session,
    _: T_CurrentUser,
):
    db_livro = session.scalar(select(Livro).where(Livro.id == livro_id))
    if not db_livro:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='livro não consta no MADR',
        )

    session.delete(db_livro)
    session.commit()

    return db_livro

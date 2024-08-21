from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero_madr.database import get_session
from fast_zero_madr.models import Romancista, User
from fast_zero_madr.schemas import (
    Message,
    RomancistaPublic,
    RomancistaPublicList,
    RomancistaSchema,
)
from fast_zero_madr.security import get_current_user

router = APIRouter(prefix='/romancista', tags=['romancista'])


T_Session = Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post(
    '/',
    status_code=HTTPStatus.CREATED,
    response_model=RomancistaPublic,
    responses={
        409: {
            'model': Message,
            'description': 'Conflict',
            'example': {'detail': 'Romancista já cadastrado'},
        },
        500: {'model': Message, 'description': 'Internal Server Error'},
    },
)
def create_romancista(
    romancista: RomancistaSchema, session: T_Session, _: T_CurrentUser
):
    db_romancista = session.scalar(
        select(Romancista).where(Romancista.nome == romancista.nome)
    )

    if db_romancista:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Romancista já cadastrado',
        )

    db_romancista = Romancista(nome=romancista.nome)

    session.add(db_romancista)
    session.commit()
    session.refresh(db_romancista)

    return db_romancista


@router.get('/{romancista_id}/', response_model=RomancistaPublic)
def read_romancista(
    romancista_id: int,
    session: T_Session,
    _: T_CurrentUser,
):
    db_romancista = session.scalar(
        select(Romancista).where(Romancista.id == romancista_id)
    )

    if not db_romancista:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Romancista não consta no MADR',
        )
    return db_romancista


@router.get('/', response_model=RomancistaPublicList)
def read_filter_romancistas(
    session: T_Session,
    _: T_CurrentUser,
    nome: str = Query(None),
    offset: int = Query(None),
    limit: int = Query(None),
):
    query = select(Romancista)

    if nome:
        query = query.filter(Romancista.nome.contains(nome))

    db_romancista = session.scalars(query.offset(offset).limit(limit)).all()

    return {'romancistas': db_romancista}


@router.put('/{romancista_id}/', response_model=RomancistaPublic)
def update_romancista(
    romancista_id: int,
    romancista: RomancistaSchema,
    session: T_Session,
    _: T_CurrentUser,
):
    db_romancista = session.scalar(
        select(Romancista).where(Romancista.id == romancista_id)
    )

    if not db_romancista:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Romancista não consta no MADR',
        )

    db_new = session.scalar(
        select(Romancista).where(Romancista.nome == romancista.nome)
    )

    if db_new:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='romancista já consta no MADR',
        )

    db_romancista.nome = romancista.nome
    session.commit()
    session.refresh(db_romancista)

    return db_romancista


@router.delete('/{romancista_id}/', response_model=RomancistaPublic)
def delete_romancista(
    romancista_id: int,
    session: T_Session,
    _: T_CurrentUser,
):
    db_romancista = session.scalar(
        select(Romancista).where(Romancista.id == romancista_id)
    )
    if not db_romancista:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Romancista não consta no MADR',
        )

    session.delete(db_romancista)
    session.commit()

    return db_romancista

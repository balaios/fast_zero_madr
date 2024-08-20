from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero_madr.database import get_session
from fast_zero_madr.models import Novelist, User
from fast_zero_madr.schemas import (
    Message,
    NovelistPublic,
    NovelistPublicList,
    NovelistSchema,
)
from fast_zero_madr.security import get_current_user

router = APIRouter(prefix='/novelists', tags=['novelists'])


T_Session = Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post(
    '/',
    status_code=HTTPStatus.CREATED,
    response_model=NovelistPublic,
    responses={
        409: {
            'model': Message,
            'description': 'Conflict',
            'example': {'detail': 'Romancista já cadastrado'},
        },
        500: {'model': Message, 'description': 'Internal Server Error'},
    },
)
def create_novelist(
    novelist: NovelistSchema, session: T_Session, _: T_CurrentUser
):
    db_novelist = session.scalar(
        select(Novelist).where(Novelist.name == novelist.name)
    )

    if db_novelist:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Romancista já cadastrado',
        )

    db_novelist = Novelist(name=novelist.name)

    session.add(db_novelist)
    session.commit()
    session.refresh(db_novelist)

    return db_novelist


@router.get('/{novelist_id}/', response_model=NovelistPublic)
def read_novelist(
    novelist_id: int,
    session: T_Session,
    _: T_CurrentUser,
):
    db_novelist = session.scalar(
        select(Novelist).where(Novelist.id == novelist_id)
    )

    if not db_novelist:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Romancista não consta no MADR',
        )
    return db_novelist


@router.get('/', response_model=NovelistPublicList)
def read_filter_novelists(
    session: T_Session,
    _: T_CurrentUser,
    name: str = Query(None),
    offset: int = Query(None),
    limit: int = Query(None),
):
    query = select(Novelist)

    if name:
        query = query.filter(Novelist.name.contains(name))

    db_novels = session.scalars(query.offset(offset).limit(limit)).all()

    return {'novelists': db_novels}


@router.put('/{novelist_id}/', response_model=NovelistPublic)
def update_novelist(
    novelist_id: int,
    novelist: NovelistSchema,
    session: T_Session,
    _: T_CurrentUser,
):
    db_novelist = session.scalar(
        select(Novelist).where(Novelist.id == novelist_id)
    )

    if not db_novelist:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Romancista não consta no MADR',
        )

    db_novelist.name = novelist.name
    session.commit()
    session.refresh(db_novelist)

    return db_novelist


@router.delete('/{novelist_id}/', response_model=NovelistPublic)
def delete_novelist(
    novelist_id: int,
    session: T_Session,
    _: T_CurrentUser,
):
    db_novelist = session.scalar(
        select(Novelist).where(Novelist.id == novelist_id)
    )
    if not db_novelist:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Romancista não consta no MADR',
        )

    session.delete(db_novelist)
    session.commit()

    return db_novelist

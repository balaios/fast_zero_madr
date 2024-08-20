from datetime import datetime
from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero_madr.database import get_session
from fast_zero_madr.models import Book, User
from fast_zero_madr.schemas import (
    BookPublic,
    BookPublicList,
    BookSchema,
    Message,
)
from fast_zero_madr.security import get_current_user

router = APIRouter(prefix='/books', tags=['books'])


T_Session = Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post(
    '/',
    status_code=HTTPStatus.CREATED,
    response_model=BookPublic,
    responses={
        409: {
            'model': Message,
            'description': 'Conflict',
            'example': {'detail': 'Romancista já cadastrado'},
        },
        500: {'model': Message, 'description': 'Internal Server Error'},
    },
)
def create_book(book: BookSchema, session: T_Session, _: T_CurrentUser):
    db_book = session.scalar(select(Book).where(Book.title == book.title))

    if db_book:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Romancista já cadastrado',
        )

    db_book = Book(
        title=book.title, year=book.year, novelist_id=book.novelist_id
    )

    session.add(db_book)
    session.commit()
    session.refresh(db_book)

    return db_book


@router.get('/{book_id}/', response_model=BookPublic)
def read_book(
    book_id: int,
    session: T_Session,
    _: T_CurrentUser,
):
    db_book = session.scalar(select(Book).where(Book.id == book_id))

    if not db_book:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Livro não consta no MADR',
        )
    return db_book


@router.get('/', response_model=BookPublicList)
def read_filter_novelists(
    session: T_Session,
    _: T_CurrentUser,
    title: str = Query(None),
    year: datetime = Query(None),
    offset: int = Query(None),
    limit: int = Query(None),
):
    query = select(Book)

    if title:
        query = query.filter(Book.title.contains(title))

    db_books = session.scalars(query.offset(offset).limit(limit)).all()

    return {'books': db_books}


@router.put('/{book_id}/', response_model=BookPublic)
def update_book(
    book_id: int,
    book: BookSchema,
    session: T_Session,
    _: T_CurrentUser,
):
    db_book = session.scalar(select(Book).where(Book.id == book_id))

    if not db_book:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Romancista não consta no MADR',
        )

    for key, value in book.model_dump(exclude_unset=True).items():
        setattr(db_book, key, value)

    session.commit()
    session.refresh(db_book)

    return db_book


@router.delete('/{book_id}/', response_model=BookPublic)
def delete_book(
    book_id: int,
    session: T_Session,
    _: T_CurrentUser,
):
    db_book = session.scalar(select(Book).where(Book.id == book_id))
    if not db_book:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Livro não consta no MADR',
        )

    session.delete(db_book)
    session.commit()

    return db_book

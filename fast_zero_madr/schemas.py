from typing import Annotated

from pydantic import AfterValidator, BaseModel, ConfigDict, EmailStr

ClearUsername = Annotated[
    str,
    AfterValidator(lambda x: ' '.join(str(x).split()).lower()),
]


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: ClearUsername
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class NovelistSchema(BaseModel):
    name: str


class NovelistPublic(NovelistSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)


class NovelistPublicList(BaseModel):
    novelists: list[NovelistPublic]


class BookSchema(BaseModel):
    title: str
    year: int
    novelist_id: int


class BookPublic(BookSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)


class BookPublicList(BaseModel):
    books: list[BookPublic]

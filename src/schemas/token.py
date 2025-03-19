from pydantic import EmailStr

from schemas.base import BaseSchema


class Token(BaseSchema):
    access_token: str
    token_type: str


class TokenData(BaseSchema):
    id: int
    email: EmailStr

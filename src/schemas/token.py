from pydantic import EmailStr

from schemas.base import BaseSchema


class Token(BaseSchema):
    token: str


class TokenData(BaseSchema):
    id: int
    email: EmailStr
    expires_at: str

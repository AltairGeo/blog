from typing import Any

from pydantic import EmailStr

from schemas.base import BaseSchema
from schemas.token import Token


class RegisterSchema(BaseSchema):
    nickname: str
    email: EmailStr
    password: str


class LoginSchema(BaseSchema):
    email: EmailStr
    password: str


class ChangePasswordSchema(BaseSchema):
    old_password: str
    new_password: str


class BaseInfo(BaseSchema):
    id: int
    email: EmailStr
    nickname: str
    role: Any


class AvatarUpload(BaseSchema):
    token: Token
    file: bytes


class ChangeNameSchema(BaseSchema):
    new_name: str
    token: str

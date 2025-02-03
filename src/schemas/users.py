from schemas.base import BaseSchema
from pydantic import EmailStr
from typing import Any

class RegisterSchema(BaseSchema):
    nickname: str
    email: EmailStr
    password: str

class LoginSchema(BaseSchema):
    email: EmailStr
    password: str


class ChangePasswordSchema(BaseSchema):
    token: str
    email: EmailStr
    old_password: str
    new_password: str

class BaseInfo(BaseSchema):
    id: int
    email: EmailStr
    nickname: str
    role: Any
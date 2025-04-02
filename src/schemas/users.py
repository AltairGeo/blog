from typing import Any, Optional

from pydantic import EmailStr, Field, AnyHttpUrl
from datetime import datetime

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
    bio: Optional[str] = Field(default=None, max_length=100)
    created_at: Optional[datetime]
    avatar_path: Optional[AnyHttpUrl]


class AvatarUpload(BaseSchema):
    token: Token
    file: bytes


class ChangeNameSchema(BaseSchema):
    new_name: str
    token: str


class ChangeBIO(BaseSchema):
    bio: str = Field(max_length=100)
    usr_id: int
    usr_mail: EmailStr

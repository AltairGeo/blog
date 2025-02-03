from schemas.base import BaseSchema
from pydantic import EmailStr

class RegisterSchema(BaseSchema):
    nickname: str
    email: EmailStr
    password: str

class LoginSchema(BaseSchema):
    email: EmailStr
    password: str
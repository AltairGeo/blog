from schemas.base import BaseSchema
from pydantic import EmailStr

class UserAddSchema(BaseSchema):
    nickname: str
    email: EmailStr
    password: str
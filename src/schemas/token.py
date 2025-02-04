from schemas.base import BaseSchema
from pydantic import EmailStr
from datetime import datetime

class Token(BaseSchema):
    token: str

class TokenData(BaseSchema):
    id: int
    email: EmailStr
    expires_at: str
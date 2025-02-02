from base import BaseSchema
from pydantic import EmailStr
from typing import Optional
from datetime import datetime

class UsersSchema(BaseSchema):
    id: int
    nickname: str
    email: EmailStr
    password: str
    avatar_path: Optional[str]
    role: Optional[str]

class PostsSchema(BaseSchema):
    id: int
    title: str
    text: str
    author_id: int
    created_at: datetime
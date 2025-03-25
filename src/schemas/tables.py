from datetime import datetime
from typing import Optional

from pydantic import EmailStr
from pydantic import Field

from schemas.base import BaseSchema


class UsersSchema(BaseSchema):
    id: int
    nickname: str
    email: EmailStr
    password: str
    avatar_path: Optional[str]
    role: Optional[str]
    bio: Optional[str] = Field(default=None, max_length=100)


class PostsSchema(BaseSchema):
    id: int
    title: str
    text: str
    author_id: int
    created_at: datetime
    public: bool

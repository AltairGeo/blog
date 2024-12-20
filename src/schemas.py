from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserReg(BaseModel):
    nickname: str
    email: EmailStr
    password: str


class Login(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    token: str

class UserFToken(BaseModel):
    id: int
    email: EmailStr
    expires_at: datetime

class Post(BaseModel):
    title: str
    text: str
    created_at: datetime = datetime.now()

class CreatePost(Post):
    token: Token

class PostGet(Post):
    author: int
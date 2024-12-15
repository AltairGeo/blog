from pydantic import BaseModel, EmailStr
import datetime

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

class Post(BaseModel):
    title: str
    text: str
    created_at: datetime.datetime

class CreatePost(Post):
    token: Token

class PostGet(Post):
    author: int
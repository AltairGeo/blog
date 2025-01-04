from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserReg(BaseModel):
    nickname: str
    email: EmailStr
    password: str

class LiteUser(BaseModel):
    id: int
    nickname: str

class Login(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    token: str

class UserFToken(BaseModel):
    id: int
    email: EmailStr
    expires_at: datetime

class BasePost(BaseModel):
    id: int
    title: str
    text: str
    created_at: datetime = datetime.now()


class Post(BasePost):
    author_id: int


class CreatePost(BasePost):
    token: Token


class AvatarHashGenerate(BaseModel):
    id: int
    email: EmailStr


class AvatarHash(BaseModel):
    image_hash: str

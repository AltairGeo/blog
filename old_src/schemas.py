#  ____            _             _   _
# |  _ \ _   _  __| | __ _ _ __ | |_(_) ___
# | |_) | | | |/ _` |/ _` | '_ \| __| |/ __|
# |  __/| |_| | (_| | (_| | | | | |_| | (__
# |_|    \__, |\__,_|\__,_|_| |_|\__|_|\___|
#        |___/
#  ____       _
# / ___|  ___| |__   ___ _ __ ___   __ _ ___
# \___ \ / __| '_ \ / _ \ '_ ` _ \ / _` / __|
#  ___) | (__| | | |  __/ | | | | | (_| \__ \
# |____/ \___|_| |_|\___|_| |_| |_|\__,_|___/
#

from pydantic import BaseModel, EmailStr
from datetime import datetime, timezone

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
    author_name: str

class CreatePost(BaseModel):
    title: str
    text: str
    created_at: datetime = datetime.now(timezone.utc)
    token: Token

class AvatarHashGenerate(BaseModel):
    id: int
    email: EmailStr

class AvatarHash(BaseModel):
    image_hash: str

class ChangePass(BaseModel):
    old_password: str
    new_password: str
    token: str

class MyBaseInfo(BaseModel):
    id: int
    email: EmailStr
    nickname: str

class PostDelete(BaseModel):
    token: str
    post_id: int

class ChangePost(Token):
    post_id: int
    title: str
    text: str

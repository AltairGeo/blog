from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends, Form

import schemas
from api.depends import auth_service
from schemas.users import RegisterSchema
from services.auth import AuthService
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

router = APIRouter(
    prefix='/auth',
    tags=["Users", "Auth"]
)

oauth_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


@router.post('/register')
async def register(data: Annotated[RegisterSchema, Form()],
                   auth_service: Annotated[AuthService, Depends(auth_service)]):
    resp = await auth_service.Register(data)
    return resp


@router.post('/login')
async def login(data: Annotated[schemas.users.LoginSchema, Form()],
                auth_service: Annotated[AuthService, Depends(auth_service)]) -> schemas.token.Token:

    return await auth_service.Login(data=data)

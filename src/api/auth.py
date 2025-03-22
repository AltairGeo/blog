from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends, Form
from fastapi.security import OAuth2PasswordRequestForm

import exceptions
from api.depends import auth_service
from schemas.token import Token
from schemas.users import RegisterSchema, LoginSchema
from services.auth import AuthService

router = APIRouter(
    prefix='/auth',
    tags=["Users", "Auth"]
)


@router.post('/register')
async def register(data: Annotated[RegisterSchema, Form()],
                   auth_service: Annotated[AuthService, Depends(auth_service)]) -> Token:
    password = data.password
    resp = await auth_service.Register(data)
    if resp:
        schema_login = LoginSchema(email=data.email, password=password)
        return await auth_service.Login(data=schema_login)
    else:
        raise exceptions.base.SomethingWasWrong


@router.post('/login')
async def login(data: Annotated[OAuth2PasswordRequestForm, Depends()],
                auth_service: Annotated[AuthService, Depends(auth_service)]) -> Token:
    return await auth_service.Login(data=LoginSchema(email=data.username, password=data.password))

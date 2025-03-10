from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends

import schemas
from api.depends import auth_service
from schemas.users import RegisterSchema
from services.auth import AuthService

router = APIRouter(
    prefix='/auth',
    tags=["Users", "Auth"]
)


@router.post('/register')
async def register(data: RegisterSchema,
                   auth_service: Annotated[AuthService, Depends(auth_service)]) -> schemas.token.Token:
    resp = await auth_service.Register(data)
    return resp


@router.post('/login')
async def login(data: schemas.users.LoginSchema,
                auth_service: Annotated[AuthService, Depends(auth_service)]) -> schemas.token.Token:
    return await auth_service.Login(data=data)

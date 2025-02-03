from fastapi import APIRouter
from fastapi import Depends
from api.depends import auth_service
from services.auth import AuthService
from schemas.users import RegisterSchema
from typing import Annotated
import schemas

router = APIRouter(
    prefix='/auth',
    tags=["Users", "Auth"]
)

@router.post('/register')
async def register(data: RegisterSchema, auth_service: Annotated[AuthService, Depends(auth_service)]) -> schemas.token.Token:
    resp = await auth_service.Register(data)
    return resp
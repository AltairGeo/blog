from fastapi import APIRouter, Depends
from typing import Annotated
from services.users import UsersService
import schemas
from api.depends import users_service

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post('/all')
async def users_all(users_service: Annotated[UsersService, Depends(users_service)]):
    resp = await users_service.GetAllUsers()
    return resp

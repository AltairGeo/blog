from fastapi import APIRouter, Depends
from schemas.users import UserAddSchema
from typing import Annotated
from services.users import UsersService
from api.depends import users_service

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post('/register')
async def register(user: UserAddSchema, users_service: Annotated[UsersService, Depends(users_service)] ):
    user_id = await users_service.AddNewUser(user=user)
    return {"user_id": user_id}

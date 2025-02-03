from fastapi import APIRouter, Depends
from typing import Annotated
from services.users import UsersService
import schemas
from typing import List
from schemas.tables import PostsSchema
from api.depends import users_service

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

ann_users_service = Annotated[UsersService, Depends(users_service)]

@router.post('/change_password')
async def change_password(data: schemas.users.ChangePasswordSchema, users_service: Annotated[UsersService, Depends(users_service)]):
    resp = await users_service.ChangePassword(ch_data=data)
    return resp

@router.post('/get_self')
async def get_self(token: schemas.token.Token, users_service: ann_users_service) -> schemas.users.BaseInfo:
    return await users_service.GetSelfByToken(token=token)

@router.get('/get_user_posts')
async def get_user_posts(user_id: int, users_service: ann_users_service) -> List[PostsSchema]:
    return await users_service.GetUserPosts(user_id=user_id)


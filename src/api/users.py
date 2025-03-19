from typing import Annotated
from typing import List

from fastapi import APIRouter, Depends, UploadFile, File, Form

import schemas
from api.depends import users_service, s3_service, get_current_user
from schemas.tables import PostsSchema, UsersSchema
from services.s3 import S3Service
from services.users import UsersService

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)
ann_user_need = Annotated[UsersSchema, Depends(get_current_user)]
ann_users_service = Annotated[UsersService, Depends(users_service)]
annotated_s3_service = Annotated[S3Service, Depends(s3_service)]


@router.post('/change_password')
async def change_password(data: schemas.users.ChangePasswordSchema,
                          users_service: Annotated[UsersService, Depends(users_service)]):
    resp = await users_service.ChangePassword(ch_data=data)
    return resp


@router.post('/get_self')
async def get_self(token: schemas.token.Token, users_service: ann_users_service) -> schemas.users.BaseInfo:
    return await users_service.GetSelfByToken(token=token)


@router.get('/get_user_posts')
async def get_user_posts(user_id: int, users_service: ann_users_service) -> List[PostsSchema]:
    return await users_service.GetUserPosts(user_id=user_id)


@router.post('/avatar_upload')
async def avatar_upload(s3_service: annotated_s3_service, token: Annotated[str, Form()], image: UploadFile = File(...)):
    file2store = await image.read()

    return await s3_service.UploadAvatar(schemas.users.AvatarUpload(
        token=schemas.token.Token(token=token),
        file=file2store
    ))


@router.get('/get_avatar_by_id')
async def get_avatar_by_id(id: int, users_service: ann_users_service):
    return await users_service.GetAvatar(id=id)


@router.post('/get_avatar_by_token')
async def get_avatar_by_token(token: schemas.token.Token, users_service: ann_users_service):
    return {"path": await users_service.GetAvatar(token=token)}


@router.post('/change_name')
async def change_name(new_name, usr: ann_user_need, users_service: ann_users_service):
    return await users_service.ChangeName(email=usr.email, new_name=new_name)

from typing import Annotated
from typing import List

from fastapi import APIRouter, Depends, UploadFile, File
from pydantic import HttpUrl

import schemas
from api.depends import users_service, s3_service, get_current_user
from schemas.tables import PostsSchema, UsersSchema
from schemas.users import ChangeBIO
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
async def change_password(
        data: schemas.users.ChangePasswordSchema,
        users_service: Annotated[UsersService, Depends(users_service)],
        usr: ann_user_need
) -> bool:
    return await users_service.ChangePassword(ch_data=data, usr=usr)


@router.get('/get_self')
async def get_self(usr: ann_user_need) -> schemas.users.BaseInfo:
    return schemas.users.BaseInfo(
        id=usr.id,
        email=usr.email,
        nickname=usr.nickname,
        role=usr.role,
        bio=usr.bio,
        created_at=usr.created_at,
        avatar_path=usr.avatar_path,
    )


@router.get('/posts/{user_id}')
async def get_user_posts(user_id: int, users_service: ann_users_service) -> List[PostsSchema]:
    return await users_service.GetUserPosts(user_id=user_id)


@router.post('/avatar_upload')
async def avatar_upload(s3_service: annotated_s3_service, usr: ann_user_need, image: UploadFile = File(...)) -> HttpUrl:
    file2store = await image.read()
    return await s3_service.UploadAvatar(file=file2store, usr=usr)


@router.get('/get_avatar_by_id')
async def get_avatar_by_id(user_id: int, users_service: ann_users_service) -> HttpUrl:
    return await users_service.GetAvatar(user_id=user_id)


@router.get('/get_avatar_by_token')
async def get_avatar(usr: ann_user_need) -> HttpUrl:
    return usr.avatar_path


@router.post('/change_name')
async def change_name(new_name, usr: ann_user_need, users_service: ann_users_service) -> bool:
    return await users_service.ChangeName(email=usr.email, new_name=new_name)

@router.get('/change_bio')
async def change_bio(bio: str, usr: ann_user_need, users_service: ann_users_service):
    return await users_service.ChangeBio(ChangeBIO(bio=bio, usr_id=usr.id, usr_mail=usr.email))
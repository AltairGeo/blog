from typing import List

import exceptions
import exceptions.base
import exceptions.users
import schemas
import security
from models.models import UsersModel
from repositories.users import UsersRepository
from schemas.users import ChangeBIO


class UsersService:
    def __init__(self, users_repo: UsersRepository):
        self.users_repo: UsersRepository = users_repo()

    async def ChangePassword(self, ch_data: schemas.users.ChangePasswordSchema, usr: schemas.tables.UsersSchema):
        if ch_data.old_password == ch_data.new_password:
            raise exceptions.users.SamePasswords
        resp = await self.users_repo.update(
            {
                "password": security.utils.create_hash(ch_data.new_password)
            },
            password=security.utils.create_hash(ch_data.old_password),
            email=usr.email
        )
        if not resp:
            raise exceptions.users.UncorrectEmailOrPassword
        if resp:
            return resp


    async def GetUserPosts(self, user_id: int) -> List[schemas.tables.PostsSchema]:
        posts = await self.users_repo.GetUserPosts(user_id=user_id)
        posts.reverse()
        if posts == []:
            raise exceptions.posts.PostsNotFound
        return [i.to_schema() for i in posts]

    async def GetAvatar(self, user_id: int) -> str:
        usr: UsersModel = await self.users_repo.find_one(id=user_id)
        return usr.avatar_path

    async def ChangeName(self, email: str, new_name: str) -> bool:
        return await self.users_repo.update({"nickname": new_name}, email=email)

    async def ChangeBio(self, bio: ChangeBIO) -> bool:
        return await self.users_repo.update({"bio": bio.bio}, id=bio.usr_id, email=bio.usr_mail)

    async def GetUserById(self, user_id: int) -> schemas.users.BaseInfo:
        user: UsersModel = await self.users_repo.find_one(id=user_id)
        return schemas.users.BaseInfo(
            id=user.id,
            bio=user.bio,
            avatar_path=user.avatar_path,
            email=user.email,
            created_at=user.created_at,
            nickname=user.nickname,
            role=user.role
        )
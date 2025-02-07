import exceptions.base
import exceptions.users
from repositories.users import UsersRepository
import schemas
import exceptions
import security
from models.models import UsersModel
from typing import List


class UsersService:
    def __init__(self, users_repo: UsersRepository):
        self.users_repo: UsersRepository = users_repo()


    async def ChangePassword(self, ch_data: schemas.users.ChangePasswordSchema) -> bool:
        security.token.check_token_to_expire(schemas.token.Token(token=ch_data.token))
        decoded = security.token.decode_jwt_token(schemas.token.Token(token=ch_data.token))
        if ch_data.old_password == ch_data.new_password:
            raise exceptions.users.SamePasswords
        resp = await self.users_repo.update(
            {
                "password": security.utils.create_hash(ch_data.new_password)
            },
            password=security.utils.create_hash(ch_data.old_password),
            email=decoded.email
        )
        if not resp:
            raise exceptions.users.UncorrectEmailOrPassword
        
        if resp:
            return {"detail": "Succesfully!"}
        

    async def GetSelfByToken(self, token: schemas.token.Token) -> schemas.users.BaseInfo:
        security.token.check_token_to_expire(token=token)
        decoded = security.token.decode_jwt_token(token=token)
        resp: UsersModel = await self.users_repo.find_one(id=decoded.id)
        
        return schemas.users.BaseInfo(
            id=resp.id,
            email=resp.email,
            nickname=resp.nickname,
            role=resp.role,
        )
    

    async def GetUserPosts(self, user_id: int) -> List[schemas.tables.PostsSchema]:
        posts = await self.users_repo.GetUserPosts(user_id=user_id)
        posts.reverse()
        if posts == []:
            raise exceptions.posts.PostsNotFound
        return [i.to_schema() for i in posts]
    

    async def GetAvatar(self, token: schemas.token.Token | None = None, id: int | None = None   ):
        if token:
            decoded = security.token.decode_jwt_token(token=token)
            user_id = decoded.id
        elif id:
            user_id = id
        
        user: UsersModel = await self.users_repo.find_one(id=user_id)
        if not user.avatar_path:
            raise exceptions.users.AvatarNotFound

        return user.avatar_path
        
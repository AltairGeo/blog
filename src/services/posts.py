import exceptions.users
from repositories.posts import PostsRepository
from repositories.users import UsersRepository
from schemas.posts import CreatePost
from schemas.token import Token
from datetime import datetime, timezone
import security
import exceptions


class PostsService():
    def __init__(self, posts_repo: PostsRepository):
        self.posts_repo: PostsRepository = posts_repo()

    async def CreatePost(self, data: CreatePost):
        security.token.check_token_to_expire(Token(token=data.token))
        decoded = security.token.decode_jwt_token(Token(token=data.token))
        UsrRepo = UsersRepository()
        user = await UsrRepo.find_one(id=decoded.id, email=decoded.email)
        if not user:
            raise exceptions.users.UserNotFound 
        return await self.posts_repo.create(
            {
                "title": data.title,
                "text": data.text,
                "author_id": user.id,
                "created_at": datetime.now(timezone.utc).replace(tzinfo=None)
            }
        )

    async def GetLastPosts(self):
        resp = await self.posts_repo.get_ten_lasts()
        return resp
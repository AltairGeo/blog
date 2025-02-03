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
        security.token.check_token_to_expire(Token(data.token))
        decoded = security.token.decode_jwt_token(Token(data.token))
        UsrRepo = UsersRepository()
        user = UsrRepo.find_one(id=decoded.id, email=decoded.email)
        if not user:
            raise exceptions.users.UserNotFound 
        self.posts_repo.create(
            {
                "title": data.title.strip(),
                "text": data.text,
                "author": user,
                "created_at": datetime.now(timezone.utc)
            }
        )

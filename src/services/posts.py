from datetime import datetime, timezone
from math import ceil
from typing import List

import exceptions
import exceptions.users
from models.models import PostsModel
from repositories.posts import PostsRepository
from schemas.posts import CreatePost
from schemas.posts import DeletePostSchema, FullPost, ChangePostSchema
from schemas.tables import UsersSchema


class PostsService:
    def __init__(self, posts_repo: PostsRepository):
        self.posts_repo: PostsRepository = posts_repo()

    async def CreatePost(self, data: CreatePost, usr: UsersSchema):
        return await self.posts_repo.create(
            {
                "title": data.title,
                "text": data.text,
                "author_id": usr.id,
                "created_at": datetime.now(timezone.utc).replace(tzinfo=None)
            }
        )

    async def GetLastPosts(self):
        resp = await self.posts_repo.get_ten_lasts()
        return resp

    async def DeletePost(self, data: DeletePostSchema, usr: UsersSchema) -> bool:
        post: PostsModel = await self.posts_repo.find_one(id=data.id)

        if not post:
            raise exceptions.posts.PostNotFound

        if post.author_id != usr.id:
            raise exceptions.posts.ItsNotYour

        return await self.posts_repo.delete(id=data.id)

    async def GetPostByID(self, post_id: int) -> FullPost:
        resp: PostsModel = await self.posts_repo.get_full_post(post_id=post_id)
        print(resp.likes)
        likes = sum(1 for like in resp.likes if like.is_like)
        dislikes = sum(1 for like in resp.likes if not like.is_like)
        if not resp:
            raise exceptions.posts.PostNotFound

        return FullPost(
            id=resp.id,
            title=resp.title,
            text=resp.text,
            created_at=resp.created_at,
            author_id=resp.author_id,
            author_name=resp.author.nickname,
            likes=likes,
            dislikes=dislikes
        )

    async def GetLastPostsPage(self, page: int):
        resp: List[PostsModel] = await self.posts_repo.get_last_page_posts(page=page)
        final = []
        for i in resp:
            final.append(
                FullPost(
                    **i.to_schema().model_dump(),
                    author_name=i.author.nickname
                )
            )
        return final

    async def ChangePost(self, data: ChangePostSchema, usr: UsersSchema) -> bool:
        post: PostsModel = await self.posts_repo.find_one(id=data.post_id)
        if not post:
            raise exceptions.posts.PostNotFound
        if post.author_id != usr.id:
            raise exceptions.posts.ItsNotYour
        else:
            change = await self.posts_repo.update(
                {
                    "title": data.title,
                    "text": data.text,
                },
                id=data.post_id,
                author_id=usr.id,
            )
            return change

    async def GetPostsCount(self) -> int:
        posts = await self.posts_repo.find_all()
        posts_count = len(posts)
        return ceil(posts_count / 10)

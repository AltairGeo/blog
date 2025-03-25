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
from utils.posts import calc_likes_and_dislikes


class PostsService:
    def __init__(self, posts_repo: PostsRepository):
        self.posts_repo: PostsRepository = posts_repo()

    async def CreatePost(self, data: CreatePost, usr: UsersSchema):
        return await self.posts_repo.create(
            {
                "title": data.title,
                "text": data.text,
                "author_id": usr.id,
                "created_at": datetime.now(timezone.utc).replace(tzinfo=None),
                "public": False,
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
        if not resp:
            raise exceptions.posts.PostNotFound
        likes = calc_likes_and_dislikes(resp.likes)
        if not resp:
            raise exceptions.posts.PostNotFound

        return FullPost(
            id=resp.id,
            title=resp.title,
            text=resp.text,
            created_at=resp.created_at,
            author_id=resp.author_id,
            author_name=resp.author.nickname,
            likes=likes["likes"],
            dislikes=likes['dislikes'],
            public=resp.public,
        )

    async def GetLastPostsPage(self, page: int):
        resp: List[PostsModel] = await self.posts_repo.get_last_page_posts(page=page)
        final = []
        for i in resp:
            ratings = calc_likes_and_dislikes(i.likes)
            final.append(
                FullPost(
                    **i.to_schema().model_dump(),
                    author_name=i.author.nickname,
                    likes=ratings['likes'],
                    dislikes=ratings['dislikes']
                )
            )
        return final

    async def ChangePost(self, post_id: int, data: ChangePostSchema, usr: UsersSchema) -> bool:
        post: PostsModel = await self.posts_repo.find_one(id=post_id)
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
                id=post_id,
                author_id=usr.id,
            )
            return change

    async def GetPostsCount(self) -> int:
        posts = await self.posts_repo.find_all()
        posts_count = len(posts)
        return ceil(posts_count / 10)

    async def ChangeStatus(self, usr: UsersSchema, post_id: int, public: bool) -> bool:
        post: PostsModel = await self.posts_repo.find_one(id=post_id)
        if post.author_id != usr.id:
            raise exceptions.posts.ItsNotYour

        return await self.posts_repo.update({"public": public}, id=post_id)

    async def GetSelfPost(self, usr: UsersSchema, post_id: int):
        resp: PostsModel = await self.posts_repo.get_self_post(post_id=post_id, usr_id=usr.id)
        if not resp:
            raise exceptions.posts.PostNotFound
        likes = calc_likes_and_dislikes(resp.likes)
        if not resp:
            raise exceptions.posts.PostNotFound

        return FullPost(
            id=resp.id,
            title=resp.title,
            text=resp.text,
            created_at=resp.created_at,
            author_id=resp.author_id,
            author_name=resp.author.nickname,
            likes=likes["likes"],
            dislikes=likes['dislikes'],
            public=resp.public,
        )


from fastapi import HTTPException

from repositories.likes import LikesRepository
from models.models import PostsLikesModel

class LikesService:
    def __init__(self, likes_repo: LikesRepository):
        self.likes_repo: LikesRepository = likes_repo()

    async def like_post(self, user_id: int, post_id: int, is_like: bool):
        ex_like: PostsLikesModel = await self.likes_repo.find_one(user_id=user_id, post_id=post_id)
        if ex_like:
            if ex_like.is_like == is_like:
                raise HTTPException(400, detail="Like already set!")
            return await self.likes_repo.update(data={"is_like": is_like}, post_id=post_id, user_id=user_id)
        else:
            return await self.likes_repo.create(
                {
                    "user_id": user_id,
                    "post_id": post_id,
                    "is_like": is_like,
                }
            )
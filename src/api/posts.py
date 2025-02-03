from fastapi import APIRouter, Depends
from typing import Annotated
from services.posts import PostsService
from api.depends import posts_service
import schemas

ann_posts_service = Annotated[PostsService, Depends(posts_service)]

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.post('/create')
async def create_post(data: schemas.posts.CreatePost, posts_service: ann_posts_service):
    return await posts_service.CreatePost(data)

@router.get('/get_last_posts')
async def get_last_posts(posts_service: ann_posts_service):
    return await posts_service.GetLastPosts()

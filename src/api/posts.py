from typing import Annotated, List

from fastapi import APIRouter, Depends, BackgroundTasks

import schemas
from api.depends import posts_service, elastic_service, get_current_user
from schemas.tables import UsersSchema
from services.elastic import ElasticService
from services.posts import PostsService

ann_user_need = Annotated[UsersSchema, Depends(get_current_user)]
ann_posts_service = Annotated[PostsService, Depends(posts_service)]
ann_elastic_service = Annotated[ElasticService, Depends(elastic_service)]

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.post('/create')
async def create_post(
        data: schemas.posts.CreatePost,
        usr: ann_user_need,
        posts_service: ann_posts_service,
        search_service: ann_elastic_service,
        background_tasks: BackgroundTasks
):
    result = await posts_service.CreatePost(data, usr)
    background_tasks.add_task(search_service.AddPostToIndexById, result.id)
    return result


@router.get('/get_last_posts')
async def get_last_posts(posts_service: ann_posts_service):
    return await posts_service.GetLastPosts()


@router.delete('/delete')
async def delete_post(
        data: schemas.posts.DeletePostSchema,
        usr: ann_user_need,
        posts_service: ann_posts_service,
        search_service: ann_elastic_service,
        background_tasks: BackgroundTasks
):
    if await posts_service.DeletePost(data=data, usr=usr):
        background_tasks.add_task(search_service.remove_post, data.id)
    else:
        return False


@router.get('/get_post')
async def get_post(post_id: int, posts_service: ann_posts_service):
    return await posts_service.GetPostByID(post_id=post_id)


@router.get('/get_last_posts_page')
async def getting_last_posts_page(page: int, posts_service: ann_posts_service) -> List[schemas.posts.FullPost]:
    return await posts_service.GetLastPostsPage(page=page)


@router.put("/change_post")
async def change_post(
        new_post: schemas.posts.ChangePostSchema,
        posts_service: ann_posts_service,
        search_service: ann_elastic_service,
        background_tasks: BackgroundTasks,
        usr: ann_user_need
):
    res = await posts_service.ChangePost(new_post, usr)
    if res:
        background_tasks.add_task(
            search_service.update_post,
            new_post.post_id,
            {"title": new_post.title, "text": new_post.text})
    return res


@router.get('/count')
async def get_count_posts(posts_service: ann_posts_service) -> int:
    return await posts_service.GetPostsCount()

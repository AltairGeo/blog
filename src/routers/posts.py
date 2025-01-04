from fastapi import HTTPException, APIRouter
from db.control import PostORM
import schemas
from typing import List
import exceptions


router = APIRouter(prefix="/posts", tags=["Posts"])


@router.post("/create_post")
async def create_post(post: schemas.CreatePost):
    try:
        return await PostORM.AddPost(post=post)
    except Exception as e:
        raise HTTPException(400, str(e))
    

@router.get("/get_last_posts")
async def get_last_posts() -> List[schemas.Post]:
    return await PostORM.GetLastTenPosts()


@router.get("/get_page_lasts_posts")
async def get_page_lasts_posts(page: int) -> List[schemas.Post]:
    return await PostORM.GetLastPagePosts(page)


@router.get("/get_post_by_id")
async def get_post_by_id(ids: int) -> schemas.Post:
    if ids <= 0:
        raise exceptions.InvalidID
    result = await PostORM.GetPostById(id=ids)
    if result != None:
        return result
    else:
        raise exceptions.PostNotFound

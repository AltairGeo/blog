from fastapi import HTTPException, APIRouter
from db.control import PostORM
import schemas
from typing import List


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



from fastapi import HTTPException, APIRouter
from db.control import PostORM
import schemas


router = APIRouter(prefix="/posts", tags=["Posts"])


@router.post("/create_post")
async def create_post(post: schemas.CreatePost):
    try:
        return await PostORM.AddPost(post=post)
    except Exception as e:
        raise HTTPException(400, str(e))
    

@router.get("/get_last_posts")
async def get_last_posts():
    return await PostORM.GetLastTenPosts()
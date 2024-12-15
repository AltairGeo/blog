from fastapi import HTTPException, APIRouter
from db.control import dbORM
import schemas


router = APIRouter(prefix="/posts", tags=["Posts"])



@router.post("/create_post")
async def create_post(post: schemas.CreatePost):
    try:
        return await dbORM.AddPost(post=post)
    except Exception as e:
        raise HTTPException(400, str(e))
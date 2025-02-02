from fastapi import HTTPException, APIRouter
from db.control import PostORM
import schemas
from typing import List
from security import JwT
import exceptions

#              ____           _
#             |  _ \ ___  ___| |_ ___
#             | |_) / _ \/ __| __/ __|
#             |  __/ (_) \__ \ |_\__ \
#             |_|   \___/|___/\__|___/
#                 _                   _       _
#   ___ _ __   __| |      _ __   ___ (_)_ __ | |_ ___
#  / _ \ '_ \ / _` |_____| '_ \ / _ \| | '_ \| __/ __|
# |  __/ | | | (_| |_____| |_) | (_) | | | | | |_\__ \
#  \___|_| |_|\__,_|     | .__/ \___/|_|_| |_|\__|___/
#                        |_|

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


@router.delete('/delete_post')
async def delete_post(data: schemas.PostDelete):
    if  JwT.check_token_for_expire(schemas.Token(token=data.token)):
        res = await PostORM.DeletePostByID(data.post_id)
        return res.rowcount
    else:
        raise exceptions.TokenWasExpire
    
@router.put('/change_post')
async def change_post(data: schemas.ChangePost):
    return await PostORM.ChangePost(data=data)
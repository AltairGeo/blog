from fastapi import APIRouter, HTTPException
from fastapi import File, UploadFile, Form
from fastapi.responses import FileResponse
import security
import schemas
import exceptions
from db import Errs
from typing import Annotated
from db.control import UserORM
from db.core import create_tables
from storage import fs

router = APIRouter(prefix="/users", tags=["Users"])
fss = fs.ImageFS()

@router.post("/register")
async def register(user: schemas.UserReg):
    try:
        return await UserORM.UserAdd(user=user)
    except Errs.UserAlreadyCreate as e:
        raise HTTPException(e.status_code, str(e))


@router.post("/upload_avatar")
async def upload_avatar(token: Annotated[str, Form()], image: UploadFile = File(...)):
    image_file = await image.read()
    decoded = security.JwT.decodeJWT(token=schemas.Token(token=token))
    if security.JwT.check_for_expire(decoded.expires_at):
        hash_image = schemas.AvatarHash(image_hash=fss.AvatarSave(schemas.AvatarHashGenerate(id=decoded.id, email=decoded.email), image=image_file))
        return await UserORM.UserAvatarChange(image_hash=hash_image, token=schemas.Token(token=token))
    else:
         raise exceptions.TokenWasExpire


@router.get("/create_tables")
async def tables():
        await create_tables()


@router.post("/login")
async def login(loginData: schemas.Login):
    try:
        return await UserORM.UserLogin(loginData)
    except Errs.UserNotFound as e:
         raise HTTPException(e.status_code, str(e))
    

@router.get("/avatar_by_id")
async def get_avatar_by_id(ids: int):
    image_hash = await UserORM.GetUserAvatarHashById(id=ids)
    return FileResponse(f"{fss.OrganizePath(image_hash)}")

from fastapi import APIRouter, HTTPException
from fastapi import File, UploadFile
import security
import schemas
import exceptions
from db import Errs
from db.control import UserORM
from db.core import create_tables
from storage import fs

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/register")
async def register(user: schemas.UserReg):
    try:
        return await UserORM.UserAdd(user=user)
    except Errs.UserAlreadyCreate as e:
        raise HTTPException(e.status_code, str(e))


@router.post("/upload_avatar")
async def upload_avatar(token: str, image: UploadFile = File(...)):
    image_file = await image.read()
    decoded = security.JwT.decodeJWT(token=schemas.Token(token=token))
    if security.JwT.check_for_expire(decoded.expires_at):
        fss = fs.ImageFS()
        fss.AvatarSave(schemas.AvatarHashGenerate(id=decoded.id, email=decoded.email), image=image_file)
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
    
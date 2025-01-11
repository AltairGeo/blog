#  _   _
# | | | |___  ___ _ __ ___
# | | | / __|/ _ \ '__/ __|
# | |_| \__ \  __/ |  \__ \
#  \___/|___/\___|_|  |___/
#                 _                   _       _
#   ___ _ __   __| |      _ __   ___ (_)_ __ | |_ ___
#  / _ \ '_ \ / _` |_____| '_ \ / _ \| | '_ \| __/ __|
# |  __/ | | | (_| |_____| |_) | (_) | | | | | |_\__ \
#  \___|_| |_|\__,_|     | .__/ \___/|_|_| |_|\__|___/
#                        |_|
#
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
import os


router = APIRouter(prefix="/users", tags=["Users"])

fss = fs.ImageFS()


@router.get("/create_tables")
async def tables():
        await create_tables() # Not for prod!

#  ____    _    ____  _____
# | __ )  / \  / ___|| ____|
# |  _ \ / _ \ \___ \|  _|
# | |_) / ___ \ ___) | |___
# |____/_/   \_\____/|_____|


@router.post("/login")
async def login(loginData: schemas.Login):
    try:
        return await UserORM.UserLogin(loginData)
    except Errs.UserNotFound as e:
         raise HTTPException(e.status_code, str(e))

@router.post("/register")
async def register(user: schemas.UserReg):
    try:
        return await UserORM.UserAdd(user=user)
    except Errs.UserAlreadyCreate as e:
        raise HTTPException(e.status_code, str(e))
    
@router.get("/get_user") # Получить краткие данные пользователя по айди
async def get_user(id: int) -> schemas.LiteUser:
    return await UserORM.GetUserById(id=id)

        
@router.post('/get_self_by_token')
async def get_self(token: schemas.Token) -> schemas.MyBaseInfo:
    return await UserORM.GetMyInfo(token=token)


@router.post('/change_password')
async def chng_pass(data: schemas.ChangePass):
    await UserORM.ChangePassword(data=data)
    

#     _             _
#    / \__   ____ _| |_ __ _ _ __
#   / _ \ \ / / _` | __/ _` | '__|
#  / ___ \ V / (_| | || (_| | |
# /_/   \_\_/ \__,_|\__\__,_|_|
#

@router.post("/upload_avatar") # загрузить аватарку
async def upload_avatar(token: Annotated[str, Form()], image: UploadFile = File(...)):
    buffer = await image.read()
    decoded = security.JwT.decodeJWT(token=schemas.Token(token=token)) # декодирование токена

    if security.JwT.check_for_expire(decoded.expires_at): # проверка срока годности токена
        hash_image = schemas.AvatarHash(image_hash=fss.AvatarSave(schemas.AvatarHashGenerate(id=decoded.id, email=decoded.email), image=buffer))
        return await UserORM.UserAvatarChange(image_hash=hash_image, token=schemas.Token(token=token))
    else:
         raise exceptions.TokenWasExpire
    

@router.get("/avatar_by_id") # Аватарка по айди
async def get_avatar_by_id(ids: int):
    image_hash = await UserORM.GetUserAvatarHashById(id=ids)
    image_path = fss.OrganizePath(image_hash)
    if os.path.exists(image_path):    
        return FileResponse(image_path)
    else:
        raise HTTPException(500, "Avatar not found!")


@router.post("/avatar_by_token") # Аватарка по токену
async def get_avatar_by_token(token: schemas.Token):
    decoded = security.JwT.decodeJWT(token)
    if security.JwT.check_for_expire(date=decoded.expires_at):
        image_hash = await UserORM.GetUserAvatarHashById(id=decoded.id)
        image_path = fss.OrganizePath(image_hash)
        if os.path.exists(image_path):    
            return FileResponse(image_path)
        else:
            raise HTTPException(500, "Avatar not found!")
    else:
        raise exceptions.TokenWasExpire

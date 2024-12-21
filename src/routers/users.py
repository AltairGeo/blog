from fastapi import APIRouter, HTTPException
import schemas
from db import Errs
from db.control import dbORM
from db.core import create_tables


router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register")
async def register(user: schemas.UserReg):
    try:
        return await dbORM.UserAdd(user=user)
    except Errs.UserAlreadyCreate as e:
        raise HTTPException(e.status_code, str(e))

@router.get("/create_tables")
async def tables():
        await create_tables()


@router.post("/login")
async def login(loginData: schemas.Login):
    try:
        return await dbORM.UserLogin(loginData)
    except Errs.UserNotFound as e:
         raise HTTPException(e.status_code, str(e))
    
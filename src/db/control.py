from db.models import Users, Posts
from db.core import engine, async_session_factory
from schemas import UserReg, Login, UserFToken, Post, Token, CreatePost
from sqlalchemy import select
from security import Hashing, JwT
from db import Errs
from fastapi import HTTPException


class dbORM:
    @staticmethod
    async def UserAdd(user: UserReg) -> None:
        user.password = Hashing.create_hash(user.password)
        Usr = Users(nickname=user.nickname, email=user.email.strip(), password=user.password)
        async with async_session_factory() as session:

            query = select(Users).filter(Users.email==user.email.strip())
            result = await session.execute(query)
            if result.fetchall() != []:
                raise Errs.UserAlreadyCreate()
            else:
                session.add(Usr)
                await session.commit()
                return "Successfully!"


    @staticmethod
    async def UserLogin(user: Login)-> Token:
        hash_password = Hashing.create_hash(user.password)
        print(user.email, user.password)
        async with async_session_factory() as session:

            query = select(Users).filter_by(email=user.email.strip())
            result = await session.execute(query)
            result = result.first()
            if result is None:
                raise Errs.UserNotFound
            if result[0].email == user.email:
                if result[0].password == hash_password:
                    return JwT.generateJWT(UserFToken(id=result[0].id, email=user.email))
                else:
                    raise HTTPException(400, "Uncorrect password!")
                    
                

    @staticmethod
    async def AddPost(post: CreatePost):
        decoded_token = JwT.decodeJWT(post.token)
        async with async_session_factory() as session:
            query = select(Users).filter_by(id=decoded_token.id)
            result = await session.execute(query)
            author = result.first()[0]

            stmnt = Posts(title=post.title, text=post.text, author=author, created_at=post.created_at)
            session.add(stmnt)
            await session.commit()
            return "Successfully!"
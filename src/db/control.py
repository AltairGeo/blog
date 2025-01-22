#   ___  ____  __  __        ____ _
#  / _ \|  _ \|  \/  |      / ___| | __ _ ___ ___  ___  ___
# | | | | |_) | |\/| |_____| |   | |/ _` / __/ __|/ _ \/ __|
# | |_| |  _ <| |  | |_____| |___| | (_| \__ \__ \  __/\__ \
#  \___/|_| \_\_|  |_|      \____|_|\__,_|___/___/\___||___/
#

from db.models import Users, Posts
from db.core import async_session_factory
from schemas import UserReg, Login, UserFToken, Token, CreatePost, AvatarHash, LiteUser, ChangePass, MyBaseInfo
from sqlalchemy import select
from security import Hashing, JwT
from db import Errs
from fastapi import HTTPException
import exceptions
from datetime import datetime, timedelta
from typing import List
from storage.fs import ImageFS


def page_offset_calculation(page: int) -> int: # offset calculation for paging
    if page <= 0:
        raise exceptions.PageLessZero
    return ((page * 5) - 5)


class UserORM: # Класс для работы с пользователями
    @staticmethod
    async def UserAdd(user: UserReg) -> str:
        user.password = Hashing.create_hash(user.password)
        Usr = Users(nickname=user.nickname, email=user.email.strip(), password=user.password)
        async with async_session_factory() as session:

            query = select(Users).filter(Users.email==user.email.strip())
            result = await session.execute(query)
            if result.fetchall() != []:
                await session.rollback()
                raise Errs.UserAlreadyCreate()
            else:
                session.add(Usr)
                await session.commit()
                user_get = await session.execute(select(Users).filter_by(email=user.email.strip()))
                user_get = user_get.scalars().first()
                return JwT.generateJWT(UserFToken(id=user_get.id, email=user.email, expires_at=(datetime.now() + timedelta(hours=8))))


    @staticmethod
    async def UserLogin(user: Login)-> Token:
        hash_password = Hashing.create_hash(user.password)
        async with async_session_factory() as session:
            query = select(Users).filter_by(email=user.email.strip())
            result = await session.execute(query)
            result = result.first()
            if result is None:
                raise Errs.UserNotFound
            if result[0].email == user.email:
                if result[0].password == hash_password:
                    return JwT.generateJWT(UserFToken(id=result[0].id, email=user.email, expires_at=(datetime.now() + timedelta(hours=8))))
                else:
                    raise HTTPException(400, "Uncorrect password!")

    @staticmethod
    async def UserAvatarChange(image_hash: AvatarHash, token: Token):
        if JwT.check_token_for_expire(token):
            decode = JwT.decodeJWT(token)
            async with async_session_factory() as session:
                stmnt = select(Users).filter_by(id=decode.id)
                res = await session.execute(stmnt)
                usr = res.scalars().first()
                if usr:
                    print(f"OLD: {usr.avatar_path}")
                    print(f"NEW: {image_hash.image_hash}")
                    if usr.avatar_path != None:
                        if usr.avatar_path != image_hash.image_hash:
                            inx = ImageFS()
                            try:
                                inx.DelOldAvatar(usr.avatar_path)
                            except Exception as e:
                                print(f"WARNING!: {e}")
                        try:
                            usr.avatar_path = image_hash.image_hash
                            await session.commit()
                            return "Successfully!"
                        except Exception as e:
                            await session.rollback()
                else:
                    raise exceptions.UserNotFound


    @staticmethod
    async def GetUserAvatarHashById(id: int) -> str:
        async with async_session_factory() as session:
            stmnt = select(Users).filter_by(id=id)
            res = await session.execute(stmnt)
            res = res.scalars().first()
            if res is None:
                raise exceptions.UserNotFound
            return res.avatar_path

    
    @staticmethod
    async def GetUserById(id: int) -> LiteUser:
        async with async_session_factory() as session:
            stmnt = select(Users).filter_by(id=id)
            res = await session.execute(stmnt)
            res = res.scalars().first()
            if res is None:
                raise exceptions.UserNotFound
            return LiteUser(id=id, nickname=res.nickname)
        

    @staticmethod
    async def ChangePassword(data: ChangePass):
        old_hash_password = Hashing.create_hash(data.old_password.strip())
        new_hash_password = Hashing.create_hash(data.new_password.strip()) # Create hashs of passwords
        decoded_token = JwT.decodeJWT(Token(token=data.token)) # Decoding token
        async with async_session_factory() as session:
            await session.begin()
            query = select(Users).filter_by(email=decoded_token.email) 
            result = await session.execute(query)
            result = result.scalars().first()
            if result is None:
                raise exceptions.UserNotFound
            if result.email == decoded_token.email: 
                if result.password == old_hash_password:
                    result.password = new_hash_password
                    await session.commit()

    @staticmethod
    async def GetMyInfo(token: Token) -> MyBaseInfo:
        decoded_token = JwT.decodeJWT(token=token)
        async with async_session_factory() as session:
            query = select(Users).filter_by(id=decoded_token.id)
            result = await session.execute(query)
            result = result.scalars().first()
            return MyBaseInfo(
                id=result.id,
                email=result.email,
                nickname=result.nickname
            )




class PostORM: # Класс для работы с постами
    @staticmethod
    async def AddPost(post: CreatePost):
        decoded_token = JwT.decodeJWT(post.token)
        if JwT.check_for_expire(decoded_token.expires_at):
            async with async_session_factory() as session:
                query = select(Users).filter_by(id=decoded_token.id)
                result = await session.execute(query)
                author = result.first()[0]

                stmnt = Posts(title=post.title, text=post.text, author=author, created_at=post.created_at)
                session.add(stmnt)
                await session.commit()
                return "Successfully!"
        else:
            raise exceptions.TokenWasExpire
    
    @staticmethod
    async def GetLastTenPosts() -> List[Posts]:
        async with async_session_factory() as session:
            stmnt = select(Posts).order_by(Posts.created_at.desc()).limit(20)
            result = await session.execute(stmnt)
            result = result.scalars().all()
            if result == []:
                raise exceptions.PostsNotFound
            return result

    @staticmethod
    async def GetLastPagePosts(page: int) -> List[Posts]:
        offset = page_offset_calculation(page)
        print(offset)
        async with async_session_factory() as session:
            stmnt = select(Posts).order_by(Posts.created_at.desc()).offset(offset=offset).limit(20)
            result = await session.execute(stmnt)
            result = result.scalars().all()
            if result == []:
                raise exceptions.PostsNotFound
            print(result)
            return result
    
    @staticmethod
    async def GetPostById(id: int) -> Posts:
        async with async_session_factory() as session:
            stmnt = select(Posts).filter_by(id=id)
            res = await session.execute(stmnt)
            return res.scalars().first()
        

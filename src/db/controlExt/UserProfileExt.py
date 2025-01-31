import schemas
import select
from typing import List
from fastapi import HTTPException
from db.models import Users, Posts
from db.core import async_session_factory
from sqlalchemy import select


class UserProfileExt():
    @staticmethod
    async def getUserPosts(user_id: int):
        async with async_session_factory() as session:
            stmnt = select(Posts).filter_by(author_id=user_id)
            res = await session.execute(stmnt) # получение всех постов юзера
            res = res.scalars().all()
            result = [] # создание списка и последующее его переворачивание
            for i in res:
                result.append(i)
            result.reverse()
            return result
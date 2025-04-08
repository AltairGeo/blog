import logging
from typing import List

from sqlalchemy import select

from db.core import async_session_maker
from models.models import UsersModel, PostsModel
from repositories.alchemy_repo import SQLAlchemyRepository


class UsersRepository(SQLAlchemyRepository):
    model = UsersModel

    async def GetUserPosts(self, user_id: int) -> List[PostsModel]:
        try:
            async with async_session_maker() as session:
                query = select(self.model).filter_by(id=user_id)
                user = await session.execute(query)
                user = user.scalar_one()
                await session.refresh(user, ['posts'])
                for i in user.posts:
                    await session.refresh(i, ["author", "likes"])
                return user.posts
        except Exception as e:
            logging.error(str(e))
            raise e

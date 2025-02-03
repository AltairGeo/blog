from repositories.alchemy_repo import SQLAlchemyRepository
from models.models import UsersModel, PostsModel
from db.core import async_session_maker
from sqlalchemy import select
from typing import List, Optional

class UsersRepository(SQLAlchemyRepository):
    model = UsersModel

    async def GetUserPosts(self, user_id: int) -> List[PostsModel]:
        async with async_session_maker() as session:
            query = select(self.model).filter_by(id=user_id)
            user = await session.execute(query)
            user = user.scalar_one()
            await session.refresh(user, ['posts'])
            posts = user.posts
            return posts
        
    
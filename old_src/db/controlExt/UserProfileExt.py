import schemas
import select
from typing import List
import exceptions
from db.models import Users, Posts
from db.core import async_session_factory
from sqlalchemy import select


class UserProfileExt():
    """
    Расширение для для главного класса UserORM.
    
    P.S UserORM наследует данный класс
    """
    
    @staticmethod
    async def getUserPosts(user_id: int) -> List[Posts]:
        """
        Получение постов пользователя по id

        P.S не подтягивает данные автора возращает только author_id
        """
        async with async_session_factory() as session:
            stmnt = select(Posts).filter_by(author_id=user_id)
            res = await session.execute(stmnt) # получение всех постов юзера
            res = res.scalars().all()
            if res == []:
                raise exceptions.PostsNotFound
            result = [] # создание списка
            for i in res:
                result.append(i) # Добавляем в него все посты
            result.reverse() # переворачиваем список
            return result

            
            
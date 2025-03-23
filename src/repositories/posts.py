import logging
from typing import Optional, List

from sqlalchemy import select

import exceptions
import schemas
import utils
from db.core import async_session_maker
from models.models import PostsModel
from repositories.alchemy_repo import SQLAlchemyRepository


class PostsRepository(SQLAlchemyRepository):
    model = PostsModel

    async def get_ten_lasts(self):
        try:
            async with async_session_maker() as session:
                stmnt = select(self.model).order_by(self.model.created_at.desc()).limit(10)
                result = await session.execute(stmnt)
                result = result.scalars().all()
                if result == []:
                    raise exceptions.posts.PostsNotFound

                final = []

                for i in result:
                    await session.refresh(i, attribute_names=['author'])
                    username = i.author.nickname
                    final.append(  # Create schemas
                        schemas.posts.FullPost(
                            id=i.id,
                            title=i.title,
                            text=i.text,
                            created_at=i.created_at,
                            author_id=i.author_id,
                            author_name=username
                        )
                    )
                return final
        except Exception as e:
            logging.error(str(e))
            raise e

    async def get_full_post(self, post_id: int) -> Optional[PostsModel]:
        try:
            async with async_session_maker() as session:
                query = select(PostsModel).filter_by(id=post_id)
                resp = await session.execute(query)
                post = resp.scalar_one_or_none()
                await session.refresh(post, attribute_names=["author", "likes"])
                return post
        except Exception as e:
            logging.error(str(e))

    async def get_last_page_posts(self, page: int) -> List[PostsModel]:
        try:
            async with async_session_maker() as session:
                offset = utils.posts.calculation_offset(page=page)
                stmnt = select(PostsModel).order_by(PostsModel.created_at.desc()).offset(offset=offset).limit(10)
                result = await session.execute(stmnt)
                result = result.scalars().all()

                if result == []:
                    raise exceptions.posts.PostsNotFound

                for i in result:
                    await session.refresh(i, attribute_names=["author"])

                return result
        except Exception as e:
            logging.error(str(e))
            raise e

    async def get_all_posts(self) -> List[schemas.posts.FullPost]:
        try:
            async with async_session_maker() as session:
                stm = select(PostsModel)
                res = await session.execute(stm)
                result = res.scalars().all()

                if result == []:
                    raise exceptions.posts.PostsNotFound

                for i in result:
                    await session.refresh(i, attribute_names=["author"])

                ready = []
                [ready.append(
                    schemas.posts.FullPost(
                        id=i.id,
                        title=i.title,
                        text=i.text,
                        author_id=i.author_id,
                        author_name=i.author.nickname,
                        created_at=i.created_at
                    )) for i in result]
                return ready
        except Exception as e:
            logging.error(str(e))
            raise e

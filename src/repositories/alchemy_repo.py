from repositories.base import AbstractRepo
from db.core import async_session_maker
from sqlalchemy import insert, update, delete, select

class SQLAlchemyRepository(AbstractRepo):
    model = None

    async def create(self, data: dict):
        async with async_session_maker() as session:
            stmt = insert(self.model).values(**data).returning(self.model)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one()  
    
    async def update(self, data: dict, **filters):
        async with async_session_maker() as session:
            stmt = update(self.model).values(**data).filter_by(**filters).returning(self.model)
            res = await session.execute(stmt)
            await session.commit()
            updated = res.scalar_one_or_none()
            return updated is not None
    
    async def delete(self, **filters) -> bool:
        async with async_session_maker() as session:
            stmt = delete(self.model).filter_by(**filters)
            res = await session.execute(stmt)
            await session.commit()
            return res.rowcount > 0

    async def find_one(self, **filters):
        async with async_session_maker() as session:
            row = await session.execute(select(self.model).filter_by(**filters))
            return row.scalar_one_or_none()

    async def find_all(self):
        async with async_session_maker() as session:
            res = await session.execute(select(self.model))
            return res.scalars().all()
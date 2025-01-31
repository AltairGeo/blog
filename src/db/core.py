#   ____ ___  ____  _____
#  / ___/ _ \|  _ \| ____|
# | |  | | | | |_) |  _|
# | |__| |_| |  _ <| |___
#  \____\___/|_| \_\_____|
#

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from db.models import *
from config import settings

engine = create_async_engine(
    settings.db_url,
    pool_size=20,
    max_overflow=0,
    pool_recycle=300,  # Пересоздавать соединения каждые 5 минут
    pool_pre_ping=True  # Проверять соединение перед использованием
    )
async_session_factory = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

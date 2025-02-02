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
    pool_size=20, # Размер пула
    max_overflow=0,
    pool_recycle=300,  # Пересоздавать соединения каждые 5 минут
    pool_pre_ping=True  # Проверять соединение перед использованием
    )
async_session_factory = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def create_tables():
    """
    Not used, but work!

    Функция для создания всех таблиц в бд.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def delete_tables():
    """
    Not used, but work!

    Функция для удаления всех таблиц в бд.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

import logging

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase

from settings import AppSettings

try:
    engine = create_async_engine(AppSettings.db_url, pool_size=20, max_overflow=0, pool_recycle=300,
                                 pool_pre_ping=True)  # Create engine
except Exception as e:
    logging.warning("Error with create db connection with production settings.")
    try:
        engine = create_async_engine(AppSettings.db_url)
    except Exception as e:
        logging.error(f"Error with creation db engine: {e}")
        raise e
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)  # Create session maker


class ModelBase(DeclarativeBase, AsyncAttrs):
    pass


async def get_async_session():
    async with async_session_maker() as session:
        yield session

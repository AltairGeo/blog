from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase
from config import AppSettings

engine = create_async_engine(AppSettings.db_url,pool_size=20, max_overflow=0, pool_recycle=300, pool_pre_ping=True ) # Create engine
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)  # Create session maker

class ModelBase(DeclarativeBase, AsyncAttrs):
    pass


async def get_async_session():
    async with async_session_maker() as session:
        yield session   
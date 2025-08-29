from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine
from core.config import get_app_config
from base.models import BaseORM
config = get_app_config()


engine = create_async_engine(config.db_uri)
session_factory = async_sessionmaker(bind=engine, expire_on_commit=False)


async def get_session() -> AsyncSession:
    async with session_factory() as session:
        yield session


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(BaseORM.metadata.create_all)
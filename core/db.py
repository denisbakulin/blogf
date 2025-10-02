from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)

from core.model import BaseORM
from core.settings import AppSettings
from functools import lru_cache


config = AppSettings.get()

@lru_cache
def get_engine():
    return create_async_engine(config.db_uri)

session_factory = async_sessionmaker(bind=get_engine(), expire_on_commit=False)


async def get_session() -> AsyncSession:
    async with session_factory() as session:
        yield session


async def init_models():
    async with get_engine().begin() as conn:
        await conn.run_sync(BaseORM.metadata.create_all)


from typing import Annotated

from fastapi import Depends

getSessionDep = Annotated[AsyncSession, Depends(get_session)]

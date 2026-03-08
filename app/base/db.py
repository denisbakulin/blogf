from pathlib import Path
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)

from base.model import BaseORM

data_dir = Path(__file__).parent.parent.parent / "data"
data_dir.mkdir(exist_ok=True)


DB_PATH = data_dir / "blogf.db"


engine = create_async_engine(
    url=f"sqlite+aiosqlite:///{DB_PATH}",
    echo=True
)

session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)


async def get_session() -> AsyncSession:
    async with session_maker() as session:
        yield session


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(BaseORM.metadata.create_all)



getSessionDep = Annotated[AsyncSession, Depends(get_session)]

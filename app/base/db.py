from pathlib import Path
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)

from base.model import BaseORM

# Создаем папку data если её нет
data_dir = Path(__file__).parent.parent.parent / "data"
data_dir.mkdir(exist_ok=True)

# Путь к базе данных в папке data
DB_PATH = data_dir / "blogf.db"

# Подключение к SQLite
engine = create_async_engine(
    url=f"sqlite+aiosqlite:///{DB_PATH}",
    echo=True
)

session_factory = async_sessionmaker(bind=engine, expire_on_commit=False)


async def get_session() -> AsyncSession:
    async with session_factory() as session:
        yield session


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(BaseORM.metadata.create_all)



getSessionDep = Annotated[AsyncSession, Depends(get_session)]

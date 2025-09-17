from sqlalchemy.ext.asyncio import AsyncSession
from core.models import BaseORM
from typing import Type, Optional

from sqlalchemy import select



class BaseRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def _get_by(
            self,
            table: Type[BaseORM],
            offset: Optional[int] = 0,
            limit: Optional[int] = 10,
            **filters,
    ) -> list[BaseORM] | None:

        stmt = select(table).filter_by(**filters)

        result = await self.session.execute(stmt.offset(offset).limit(limit))

        items = result.scalars().all()

        return list(items)












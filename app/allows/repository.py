from sqlalchemy.ext.asyncio import AsyncSession

from allows.model import Allow
from base.repository import BaseRepository


class AllowRepository(BaseRepository[Allow]):
    def __init__(self, session: AsyncSession):
        super().__init__(model=Allow, session=session)



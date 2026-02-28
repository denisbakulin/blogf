from base.repository import BaseRepository
from entities.subscribe import Subscribe
from sqlalchemy.ext.asyncio import AsyncSession

class SubscribeRepository(BaseRepository[Subscribe]):
    def __init__(self, session: AsyncSession):
        super().__init__(Subscribe, session)



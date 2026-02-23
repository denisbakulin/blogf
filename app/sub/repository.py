from base.repository import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sub.model import Subscribe


class SubscribeRepository(BaseRepository[Subscribe]):

    def __init__(self, session: AsyncSession):
        super().__init__(Subscribe, session)
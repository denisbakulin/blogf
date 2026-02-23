from base.repository import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession
from topic.offrer.model import TopicOffer


class TopicOfferRepository(BaseRepository[TopicOffer]):

    def __init__(self, session: AsyncSession):
        super().__init__(TopicOffer, session)

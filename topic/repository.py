from topic.model import Topic, TopicOffer
from core.repository import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession



class TopicRepository(BaseRepository[Topic]):

    def __init__(self, session: AsyncSession):
        super().__init__(Topic, session)



class TopicOfferRepository(BaseRepository[TopicOffer]):

    def __init__(self, session: AsyncSession):
        super().__init__(TopicOffer, session)








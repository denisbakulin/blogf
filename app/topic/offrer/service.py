from base.service import BaseService
from sqlalchemy.ext.asyncio import AsyncSession
from topic.offrer.model import TopicOffer
from topic.offrer.repository import TopicOfferRepository
from topic.offrer.schemas import CreateTopicOffer
from user.model import User


class TopicOfferService(BaseService[TopicOffer, TopicOfferRepository]):

    def __init__(self, session: AsyncSession):
        super().__init__(TopicOffer, session, TopicOfferRepository)

    async def create_offer_topic(self, author: User, topic_create: CreateTopicOffer) -> TopicOffer:
        return await self.create_item(
            author_id=author.id, **topic_create.dict()
        )

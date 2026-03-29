from base.service import BaseService
from entities import TopicOffer
from helpers.search import Pagination
from repositories import TopicOfferRepository
from schemas.topic_offer import CreateTopicOffer
from sqlalchemy.ext.asyncio import AsyncSession


class TopicOfferService(BaseService[TopicOffer, TopicOfferRepository]):

    def __init__(self, session: AsyncSession):
        super().__init__(TopicOffer, session, TopicOfferRepository)

    async def create_offer_topic(self, author_id: int, topic_create: CreateTopicOffer) -> TopicOffer:
        return await self.create_item(author_id=author_id, **topic_create.dict())

    async def get_topic_offer_by_id(self, offer_id):
        return self.ensure_one_return(
            await self.repository.get_topic_offer_by_id(offer_id)
        )

    async def get_topic_offers(self, pagination: Pagination):
        return await self.repository.get_some_topic_offers(**pagination.dict())



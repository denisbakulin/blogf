from base.service import BaseService
from models.topic_offer import TopicOffer
from repositories.topic_offer import TopicOfferRepository
from schemas.topic_offer import CreateTopicOffer
from sqlalchemy.ext.asyncio import AsyncSession
from DTO.topic_offer import FullTopicOfferDTO, TopicOfferDTO
from helpers.search import Pagination

class TopicOfferService(BaseService[TopicOffer, TopicOfferRepository, TopicOfferDTO]):

    def __init__(self, session: AsyncSession):
        super().__init__(TopicOffer, session, TopicOfferRepository)

    async def create_offer_topic(self, author_id: int, topic_create: CreateTopicOffer) -> TopicOfferDTO:
        return await self.create_item(author_id=author_id, **topic_create.dict())

    async def get_topic_offer_by_id(self, offer_id) -> FullTopicOfferDTO:
        return await self.repository.get_topic_offer_by_id(offer_id)

    async def get_topic_offers(self, pagination: Pagination) -> list[FullTopicOfferDTO]:
        return await self.repository.get_some_topic_offers(**pagination.dict())



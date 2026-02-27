from base.repository import BaseRepository
from models.topic_offer import TopicOffer
from sqlalchemy.ext.asyncio import AsyncSession
from DTO.topic_offer import TopicOfferDTO, FullTopicOfferDTO
from models.user import User
from utils.default import to_dto
from sqlalchemy import select
from dataclasses import asdict
from sqlalchemy.sql import Select
from sqlalchemy.orm import aliased

# Создаем два разных алиаса для одной таблицы User
Author = aliased(User, name="author")
Processor = aliased(User, name="processor")


class TopicOfferRepository(BaseRepository[TopicOffer, TopicOfferDTO]):
    def __init__(self, session: AsyncSession):
        super().__init__(TopicOffer, session, TopicOfferDTO)

    def get_full_offer_stmt(self) -> Select:
        return (
            select(
                TopicOffer,
                Author.username.label("author_name"),
                Processor.username.label("process_name")
            )
            .join(Author, TopicOffer.author_id == Author.id)
            .outerjoin(Processor, TopicOffer.process_user_id == Processor.id)
        )


    async def get_topic_offer_by_id(self, offer_id: int) -> FullTopicOfferDTO:

        stmt = self.get_full_offer_stmt().where(TopicOffer.id == offer_id)
        result = await self.session.execute(stmt)

        offer, author, process = result.first()
        dto_topic = to_dto(offer, TopicOfferDTO)

        return FullTopicOfferDTO(
            author_username=author,
            process_user_username=process,
            **asdict(dto_topic)
        )

    async def get_some_topic_offers(
            self, offset: int | None = None,
            limit: int | None = None
    ) -> list[FullTopicOfferDTO]:

        stmt = self.get_full_offer_stmt()
        stmt = self.paginator(stmt, offset, limit)

        result = await self.session.execute(stmt)
        offers = result.all()

        return [
            FullTopicOfferDTO(
                author_username=author,
                process_user_username=process,
                **asdict(to_dto(offer, TopicOfferDTO))
            ) for offer, author, process in offers
        ]







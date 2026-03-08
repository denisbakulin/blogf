from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased
from sqlalchemy.sql import Select

from base.repository import BaseRepository
from entities.topic_offer import TopicOffer
from entities.user import User

Author = aliased(User, name="author")
Processor = aliased(User, name="processor")


class TopicOfferRepository(BaseRepository[TopicOffer]):
    def __init__(self, session: AsyncSession):
        super().__init__(TopicOffer, session)

    def get_full_offer_stmt(self) -> Select:
        return (
            select(
                TopicOffer, Author, Processor
            )
            .join(Author, TopicOffer.author_id == Author.id)
            .outerjoin(Processor, TopicOffer.process_user_id == Processor.id)
        )


    async def get_topic_offer_by_id(
            self, offer_id: int
    ) -> tuple[TopicOffer, Author, Processor]:

        stmt = self.get_full_offer_stmt().where(TopicOffer.id == offer_id)
        result = await self.session.execute(stmt)

        offer, author, process = result.first()

        return (offer, author, process)


    async def get_some_topic_offers(
            self, offset: int | None = None,
            limit: int | None = None
    ) -> list[tuple[TopicOffer, Author, Processor]]:

        stmt = self.get_full_offer_stmt()
        stmt = self.process_paginate_stmt(stmt, offset, limit)

        result = await self.session.execute(stmt)

        return [
            (offer, author, process) for offer, author, process in result.all()
        ]







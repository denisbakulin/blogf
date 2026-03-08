from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from base.repository import BaseRepository
from entities.post import Post
from entities.reaction import Reaction, ReactionType


class ReactionRepository(BaseRepository[Reaction]):

    def __init__(self, session: AsyncSession):
        super().__init__(Reaction, session)

    async def get_post_reaction_count(self, post_id: int) -> dict[ReactionType, int]:
        stmt = (
            select(
                Reaction.type,
                func.count()
            )
            .where(Reaction.post_id == post_id)
            .group_by(Reaction.type)
        )

        result = await self.session.execute(stmt)

        return {
            r_type: count
            for r_type, count in result.all()
        }


    async def get_container_reaction_count(self, topic_id: int):
        stmt = (
            select(
                Reaction.type,
                func.count()
            )
            .join(
                Post, Reaction.container_id == topic_id
            )
            .where(Reaction.post_id == topic_id)
            .group_by(Reaction.type)
        )

        result = await self.session.execute(stmt)

        return {
            reaction: count
            for reaction, count in result.all()
        }



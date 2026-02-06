from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from base.repository import BaseRepository
from post.model import Post
from reaction.model import Reaction
from container.model import Container


class ReactionRepository(BaseRepository[Reaction]):

    def __init__(self, session: AsyncSession):
        super().__init__(Reaction, session)

    async def get_post_reaction_count(self, post: Post) -> dict[str, int]:
        stmt = (
            select(
                Reaction.reaction,
                func.count().label("count")
            )
            .where(Reaction.post_id == post.id)
            .group_by(Reaction.reaction)
        )

        result = await self.session.execute(stmt)

        return {reaction: count for reaction, count in result.all()}

    async def get_topic_reaction_count(self, topic: Container):
        stmt = (
            select(
                Reaction.reaction,
                func.count().label("count")
            )
            .join(
                Post, Reaction.container_id == topic.id
            )
            .where(Reaction.post_id == topic.id)
            .group_by(Reaction.reaction)
        )

        result = await self.session.execute(stmt)

        return {reaction: count for reaction, count in result.all()}



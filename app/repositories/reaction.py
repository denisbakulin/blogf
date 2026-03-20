from base.repository import BaseRepository
from entities.post import Post
from entities.reaction import Reaction, ReactionType
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from entities.user import User

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

    async def get_post_reactions(
            self, post_id: int,
            type_: ReactionType | None = None,
            offset: int | None = None,
            limit: int | None = None
    ) -> list[tuple[Reaction, User]]:
        stmt = (
            select(Reaction, User)
            .join(User, Reaction.author_id == User.id)
            .join(Post, Reaction.post_id == Reaction.post_id)
            .where(Post.id == post_id)
            .where(Reaction.type == type_)
        )
        stmt = self.process_paginate_stmt(stmt, offset, limit)
        result = await self.session.execute(stmt)

        return [
            (reaction, user)
            for reaction, user in result.all()
        ]


    async def get_user_reactions(
            self, user_id: int,
            type_: ReactionType | None = None,
            offset: int | None = None,
            limit: int | None = None
    ) -> list[tuple[Reaction, Post]]:
        stmt = (
            select(Reaction, Post)
            .join(User, Reaction.author_id == User.id)
            .join(Post, Reaction.post_id == Reaction.post_id)
            .where(User.id == user_id)
            .where(Reaction.type == type_)
        )
        stmt = self.process_paginate_stmt(stmt, offset, limit)
        result = await self.session.execute(stmt)

        return [
            (reaction, post)
            for reaction, post in result.all()
        ]


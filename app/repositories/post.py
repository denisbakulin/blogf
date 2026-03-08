from sqlalchemy import desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from base.repository import BaseRepository
from entities.container import Container, ContainerType
from entities.post import Post
from entities.reaction import Reaction, ReactionType
from entities.user import User

POST_FULL = [
    Post, User, Container
]

class PostRepository(BaseRepository[Post]):

    def __init__(self, session: AsyncSession):
        super().__init__(Post, session)


    async def get_top_of_topic_posts(
            self, container_type: ContainerType,
            reaction_type: ReactionType,
            offset: int | None = None,
            limit: int | None = None
    ) -> list[tuple[Post, User, Container, int]]:
        stmt = (
            select(
                *POST_FULL,
                func.count(Reaction.post_id).label("count")
            )
            .join(Reaction, Reaction.post_id == Post.id)
            .join(Container, Post.container_id == Container.id)
            .join(User, Post.author_id == User.id)
            .where(Container.type == container_type)
            .where(Reaction.type == reaction_type)
            .group_by(Post.id)
            .order_by(desc("count"))
        )
        stmt = self.process_paginate_stmt(stmt, offset, limit)

        result = await self.session.execute(stmt)

        return [
             (post, user, container, count)
             for post, user, container, count in result.all()
        ]


    async def get_container_posts(
            self, container_id: int,
            offset: int | None = None,
            limit: int | None = None
        ) -> list[tuple[Post, User]]:
        stmt = (
            select(
                Post, User
            )
            .join(Container, Post.container_id == Container.id)
            .join(User, Post.author_id == User.id)
            .where(Post.container_id == container_id)
        )

        stmt = self.process_paginate_stmt(stmt, offset, limit)

        result = await self.session.execute(stmt)

        return [
            (post, user)
            for post, user in result.all()
        ]






from base.repository import BaseRepository
from entities import Container, Post, Subscribe, User

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class SubscribeRepository(BaseRepository[Subscribe]):
    def __init__(self, session: AsyncSession):
        super().__init__(Subscribe, session)

    async def get_user_subs(self, user_id: int, offset: int, limit: int):
        stmt = (
            select(Container)
            .join(Subscribe, Subscribe.container_id == Container.id)
            .where(Subscribe.user_id == user_id)
        )
        stmt = self.process_paginate_stmt(stmt, offset, limit)
        result = await self.session.execute(stmt)

        return result.scalars().all()

    async def get_user_content(self, user_id: int, offset: int, limit: int):
        stmt = (
            select(Post, Container)
            .join(Subscribe, Post.container_id == Subscribe.container_id)
            .join(Container, Post.container_id == Container.id)
            .where(Subscribe.user_id == user_id)
        )

        stmt = self.process_paginate_stmt(stmt, offset, limit)

        result = await self.session.execute(stmt)

        return result.scalars().all()

    async def get_container_subscribers(self, container_id: int,  offset: int, limit: int):
        stmt = (
            select(User)
            .join(Subscribe, User.id == Subscribe.user_id)
            .where(Subscribe.container_id == container_id)
        )

        stmt = self.process_paginate_stmt(stmt, offset, limit)

        result = await self.session.execute(stmt)

        return result.scalars().all()

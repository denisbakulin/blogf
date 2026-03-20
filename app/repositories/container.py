from typing import Any

from base.repository import BaseRepository
from entities.comment import Comment
from entities.container import Container, ContainerType
from entities.post import Post
from entities.user import User
from sqlalchemy import distinct, func, select
from sqlalchemy.ext.asyncio import AsyncSession

full_container_stmt = (
    select(
        Container, User
    )
    .join(User, Container.author_id == User.id)
)

metrics_stmt = (
    select(Container, User, func.count(distinct(Post.id)), func.count(Comment.id))
    .select_from(Container)
    .join(
        User, Container.author_id == User.id
    )
    .outerjoin(
        Post, Container.id == Post.container_id
    )
    .outerjoin(
        Comment, Comment.post_id == Post.id
    )
    .group_by(Container.id)
)


class ContainerRepository(BaseRepository[Container]):

    def __init__(self, session: AsyncSession):
        super().__init__(Container, session)


    async def get_metrics_container(self, container_id: int) -> (Container, User, int, int):
        stmt = metrics_stmt.where(Container.id == container_id)
        result = await self.session.execute(stmt)

        container, user, post_count, comment_count = result.first()

        return (container, user, post_count, comment_count)

    async def get_metrics_containers(self,
            offset: int | None = None,
            limit: int | None = None
    ) -> list[tuple[Container, User, int, int]]:
        stmt = self.process_paginate_stmt(metrics_stmt, offset, limit)

        result = await self.session.execute(stmt)

        return [
            (container, user, post_count, comment_count)
            for container, user, post_count, comment_count in result.all()
        ]



    async def get_full_container(self, container_id: int) -> tuple[Container, User]:
        stmt = full_container_stmt.where(Container.id == container_id)

        result = await self.session.execute(stmt)
        container, user = result.first()

        return (container, user)

    async def search(
            self, field: str,
            value: Any,
            strict: bool,
            type_: ContainerType,
            offset: int | None = None,
            limit: int | None = None
    ) -> list[Container]:

        stmt = select(Container).where(Container.type == type_)
        stmt = self.process_search_stmt(stmt, strict, field, value)
        stmt = self.process_paginate_stmt(stmt, offset, limit)

        result = await self.session.execute(stmt)

        return [
            (container, user)
            for container, user in result.all()
        ]








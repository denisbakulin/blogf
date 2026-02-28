from base.repository import BaseRepository
from models.comment import Comment
from models.container import Container, ContainerType
from models.post import Post
from sqlalchemy import distinct, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any
from models.user import User
from DTO.container import MetricsContainerDTO, ContainerDTO, ContainerWithAuthorDTO
from dataclasses import asdict

from utils.default import to_dto


class ContainerRepository(BaseRepository[Container, ContainerDTO]):

    def __init__(self, session: AsyncSession):
        super().__init__(Container, session, ContainerDTO)


    def get_metrics_stmt(self):
        return (
            select(Container, User.username, func.count(distinct(Post.id)), func.count(Comment.id))
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

    def to_metrics_container_dto(self, container: tuple[Container, str, int, int]):
        container, username, post_count, comment_count = container
        return MetricsContainerDTO(
            container=ContainerWithAuthorDTO(
                **asdict(to_dto(container, ContainerDTO)),
                author_username=username
            ),
            post_count=post_count,
            comment_count=comment_count,
        )

    async def get_metrics_container(self, container_id: int) -> MetricsContainerDTO:
        stmt = self.get_metrics_stmt().where(Container.id == container_id)
        res = await self.session.execute(stmt)
        return self.to_metrics_container_dto(res.tuples().first())

    async def get_metrics_containers(self,
            offset: int | None = None,
            limit: int | None = None
    ) -> list[MetricsContainerDTO]:
        stmt = self.get_metrics_stmt()
        stmt = self.process_paginate_stmt(stmt, offset, limit)

        res = await self.session.execute(stmt)
        return list(self.to_metrics_container_dto(c) for c in res.tuples().all())

    def get_full_container_stmt(self):
        return (
            select(
                Container,
                User.username
            )
            .join(User, Container.author_id == User.id)
        )

    async def get_full_container(self, container_id) -> ContainerWithAuthorDTO:
        stmt = self.get_full_container_stmt().where(Container.id == container_id)

        res = await self.session.execute(stmt)
        container, username = res.first()

        return ContainerWithAuthorDTO(
            **asdict(to_dto(container, ContainerDTO)),
            author_username=username
        )

    async def search(
            self, field: str,
            value: Any,
            strict: bool,
            type_: ContainerType,
            offset: int | None = None,
            limin: int | None = None
    ) -> list[ContainerWithAuthorDTO]:
        stmt = self.get_full_container_stmt().where(Container.type == type_)

        stmt = self.process_search_stmt(stmt, strict, field, value)
        stmt = self.process_paginate_stmt(stmt, offset, limin)

        res = await self.session.execute(stmt)

        containers = res.all()

        return [
            ContainerWithAuthorDTO(
                **asdict(to_dto(container, ContainerDTO)),
                author_username=username
            ) for container, username in containers
        ]








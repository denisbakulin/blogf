from base.repository import BaseRepository
from entities import Container, ContainerType, User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

full_container_stmt = (
    select(
        Container, User
    )
    .join(User, Container.author_id == User.id)
)



class ContainerRepository(BaseRepository[Container]):

    def __init__(self, session: AsyncSession):
        super().__init__(Container, session)


    async def get_metrics_container(self,type_: ContainerType, container_id: int) -> tuple[Container, User]:
        stmt = (
            full_container_stmt
            .where(Container.id == container_id)
            .where(Container.type == type_)
        )
        result = await self.session.execute(stmt)

        container, user, post_count, comment_count = result.first()

        return (container, user)

    async def get_metrics_containers(self,
            type_: ContainerType,
            offset: int | None = None,
            limit: int | None = None,

    ) -> list[tuple[Container, User]]:

        stmt = self.process_paginate_stmt(
            full_container_stmt.where(Container.type == type_), offset, limit
        )

        result = await self.session.execute(stmt)

        return [
            (container, user)
            for container, user in result.all()
        ]



    async def get_full_container(self, container_id: int) -> tuple[Container, User]:
        stmt = full_container_stmt.where(Container.id == container_id)

        result = await self.session.execute(stmt)
        container, user = result.first()

        return (container, user)

    # async def search(
    #         self, field: str,
    #         value: Any,
    #         strict: bool,
    #         type_: ContainerType,
    #         offset: int | None = None,
    #         limit: int | None = None
    # ) -> list[Container]:
    #
    #     stmt = select(Container).where(Container.type == type_)
    #     stmt = self.process_search_stmt(stmt, strict, field, value)
    #     stmt = self.process_paginate_stmt(stmt, offset, limit)
    #
    #     result = await self.session.execute(stmt)
    #
    #     return [
    #         (container, user)
    #         for container, user in result.all()
    #     ]








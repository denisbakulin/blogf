from base.repository import BaseRepository
from models.comment import Comment
from models.container import Container
from models.post import Post
from sqlalchemy import distinct, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from DTO.container import FullContainerDTO, ContainerDTO

class ContainerRepository(BaseRepository[Container]):

    def __init__(self, session: AsyncSession):
        super().__init__(Container, session)


    async def get_containers_with_content_counts(
            self,
            offset: int | None = None,
            limit: int | None = None,
            container_id: int | None = None,

    ) -> list[FullContainerDTO] | FullContainerDTO:
        """Возвращает topic и количество постов, комментариев под ним """

        stmt = (
            select(Container, func.count(distinct(Post.id)), func.count(Comment.id))
            .select_from(Container)
            .outerjoin(
                Post, Container.id == Post.container_id
            )
            .outerjoin(
                Comment, Comment.post_id == Post.id
            )
            .group_by(Container.id)
        )

        if container_id:
            stmt = stmt.where(Container.id == container_id)
        else:
            stmt = stmt.offset(offset).limit(limit)

        res = await self.session.execute(stmt)

        if container_id:
            return self.to_full_container_dto(res.tuples().first())

        return list(self.to_full_container_dto(c) for c in res.tuples().all())

    def to_full_container_dto(self, container: tuple[Container, int, int]):
        container, post_count, comment_count = container
        return FullContainerDTO(
            container=self.to_dto(container),
            post_count=post_count,
            comment_count=comment_count
        )

    def to_dto(self, container: Container) -> ContainerDTO:
        return ContainerDTO()






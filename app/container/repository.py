from typing import TypeAlias

from base.repository import BaseRepository
from comment.model import Comment
from container.model import Container
from post.model import Post
from sqlalchemy import distinct, func, select
from sqlalchemy.ext.asyncio import AsyncSession

full_topic: TypeAlias = tuple[Container, int, int]

class ContainerRepository(BaseRepository[Container]):

    def __init__(self, session: AsyncSession):
        super().__init__(Container, session)


    async def get_containers_with_content_counts(
            self,
            offset: int | None = None,
            limit: int | None = None,
            container_id: int | None = None,

    ) -> list[full_topic] | full_topic:
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
            return res.tuples().first()

        return list(res.tuples().all())









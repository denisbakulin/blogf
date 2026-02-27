from base.repository import BaseRepository
from models.comment import Comment
from models.container import Container, ContainerType
from models.post import Post
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession


class CommentRepository(BaseRepository[Comment]):

    def __init__(self, session: AsyncSession):
        super().__init__(Comment, session)

    async def create_comment(
            self,
            **comment_data,
    ) -> Comment:
        return self.create(**comment_data)

    async def get_user_comment_count_in_topics(
            self,
            user_id: int,
    ) -> list[tuple[Container, int]]:
        stmt = (
            select(
                Container,
                func.count(Comment.id)
            )
            .join(
                Post, Post.container_id == Container.id
            )
            .join(
                Comment, Comment.post_id == Post.id
            )
            .where(Comment.user_id == user_id)
            .where(Container.type == ContainerType.topic)
            .group_by(Container.id)
            .limit(10)
        )

        result = await self.session.execute(stmt)


        return list(result.tuples().all())






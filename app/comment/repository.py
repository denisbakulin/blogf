from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from base.repository import BaseRepository
from comment.model import Comment
from post.model import Post
from container.model import Container


class CommentRepository(BaseRepository[Comment]):

    def __init__(self, session: AsyncSession):
        super().__init__(Comment, session)

    async def create_comment(
            self,
            **comment_data,
    ) -> Comment:
        return self.create(**comment_data)

    async def get_user_comment_count_by_topic(
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
            .group_by(Container.id)
            .limit(10)
        )

        result = await self.session.execute(stmt)


        return [*result.tuples().all()]






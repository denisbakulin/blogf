from core.repository import BaseRepository
from comment.models import Comment
from sqlalchemy import select
from typing import Optional


class CommentRepository(BaseRepository):

    async def create_comment(
            self,
            comment_data: dict,
            author_id: int,
            post_id: int,
            parent_id: int
    ) -> Comment:

        comment = Comment(
            **comment_data,
            author_id=author_id,
            post_id=post_id,
            parent_id=parent_id
        )
        self.session.add(comment)
        return comment

    async def get_comment(self, post_id: int) -> Optional[Comment]:
        return await self.session.get(Comment, post_id)

    async def get_comments(
            self,
            offset: Optional[int] = 0,
            limit: Optional[int] = 10,
            **filters,
    ) -> list[Comment] | None:
        return await super()._get_by(Comment, offset=offset, limit=limit, **filters)








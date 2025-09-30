from core.repository import BaseRepository
from comment.model import Comment
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession


class CommentRepository(BaseRepository[Comment]):

    def __init__(self, session: AsyncSession):
        super().__init__(Comment, session)

    async def create_comment(
            self,
            **comment_data,
    ) -> Comment:
        return self.create(**comment_data)

    async def get_comments(
            self,
            offset: Optional[int],
            limit: Optional[int],
            **filters,
    ) -> list[Comment] | None:
        return await self.get_any_by(offset=offset, limit=limit, **filters)

    async def get_comment(
            self,
            **filters
    ) -> Optional[Comment]:
        return await self.get_one_by(**filters)







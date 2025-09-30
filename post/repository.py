from core.repository import BaseRepository
from post.model import Post
from typing import Optional, Any, override
from sqlalchemy.ext.asyncio import AsyncSession

class PostRepository(BaseRepository[Post]):

    def __init__(self, session: AsyncSession):
        super().__init__(Post, session)

    def create_post(self, **post_data) -> Post:
        return self.create(**post_data)


    async def get_posts(
            self,
            offset: Optional[int],
            limit: Optional[int],
            **filters,
    ) -> list[Post] | None:

        return await self.get_any_by(offset=offset, limit=limit, **filters)


    async def search_posts(
            self,
            offset: int,
            limit: int,
            field: str,
            query: Any,
    ) -> list[Post]:
        return await self.search(field, query, offset=offset, limit=limit)








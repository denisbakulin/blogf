from core.repository import BaseRepository
from post.models import Post
from sqlalchemy import select
from typing import Optional

class PostRepository(BaseRepository):

    def create_post(self, post_data: dict, author_id: int) -> Post:
        post = Post(**post_data, author_id=author_id)
        self.session.add(post)
        return post

    async def get_post(self, post_id: int) -> Optional[Post]:
        return await self.session.get(Post, post_id)

    async def get_posts(
            self,
            offset: Optional[int] = 0,
            limit: Optional[int] = 10,
            **filter,
    ) -> list[Post] | Post | None:

        stmt = select(Post).filter_by(**filter)

        result = await self.session.execute(stmt.offset(offset).limit(limit))

        posts = result.scalars().all()

        return list(posts)







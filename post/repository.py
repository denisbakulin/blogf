from core.repository import BaseRepository
from post.models import Post
from sqlalchemy import select
from typing import Optional

class PostRepository(BaseRepository):

    def create_post(self, post_data: dict, author_id: int):
        post = Post(**post_data, author_id=author_id)
        self.session.add(post)
        return post

    async def get_post(self, post_id: int) -> Optional[Post]:
        return await self.session.get(Post, post_id)

    async def get_posts(
            self,
            title: Optional[str] = None,
            slug: Optional[str] = None,
            author_username: Optional[str] = None,
            author_id: Optional[int] = None,
            offset: Optional[int] = 0,
            limit: Optional[int] = 10
    ) -> list[Post] | Post | None:

        stmt = select(Post)

        if title:
            stmt = stmt.where(Post.title == title)
        elif slug:
            stmt = stmt.where(Post.slug == slug)
        elif author_username:
            stmt = stmt.where(Post.author.username == author_username)
        elif author_id:
            stmt = stmt.where(Post.author_id == author_id)

        else:
            return

        result = await self.session.execute(stmt.offset(offset).limit(limit))

        posts = result.scalars().all()

        return list(posts)







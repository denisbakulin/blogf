
from sqlalchemy import desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from base.repository import BaseRepository
from post.model import Post
from reaction.model import Reaction


class PostRepository(BaseRepository[Post]):

    def __init__(self, session: AsyncSession):
        super().__init__(Post, session)


    async def get_top_of_posts(self, reaction: str):
        stmt = (
            select(
                Post,
                func.count(Reaction.post_id).label("like_count")
            )
            .join(Reaction, Reaction.post_id == Post.id)
            .where(Reaction.reaction == reaction)
            .group_by(Post.id)
            .order_by(desc("like_count"))
            .limit(10)
        )
        result = await self.session.execute(stmt)

        posts = result.all()

        return list(posts)







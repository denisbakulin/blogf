
from base.repository import BaseRepository
from models.container import Container, ContainerType
from models.post import Post
from models.reaction import Reaction
from sqlalchemy import desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession


class PostRepository(BaseRepository[Post]):

    def __init__(self, session: AsyncSession):
        super().__init__(Post, session)


    async def get_top_of_topic_posts(self, reaction: str):
        stmt = (
            select(
                Post,
                func.count(Reaction.post_id).label("like_count")
            )
            .join(Reaction, Reaction.post_id == Post.id)
            .join(Container, Post.container_id == Container.id)
            .where(Reaction.reaction == reaction)
            .where(Container.type == ContainerType.topic)
            .group_by(Post.id)
            .order_by(desc("like_count"))
            .limit(10)
        )
        result = await self.session.execute(stmt)

        posts = result.all()

        return list(posts)







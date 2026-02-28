from base.repository import BaseRepository
from models.container import Container, ContainerType
from models.post import Post
from models.reaction import Reaction
from sqlalchemy import desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from DTO.post import PostDTO
from models.container import Container
from models.user import User

POST_FULL = [
    Post,
    User.username.label("author_username"),
    Container.slug.label("container_slug")
]

class PostRepository(BaseRepository[Post, PostDTO]):

    def __init__(self, session: AsyncSession):
        super().__init__(Post, session, PostDTO)


    async def get_top_of_topic_posts(
            self, type_: ContainerType,
            offset: int | None = None,
            limit: int | None = None
    ):
        stmt = (
            select(
                *POST_FULL,
                func.count(Reaction.post_id).label("like_count")
            )
            .join(Reaction, Reaction.post_id == Post.id)
            .join(Container, Post.container_id == Container.id)
            .join(User, Post.author_id == User.id)
            .where(Container.type == type_)
            .group_by(Post.id)
            .order_by(desc("like_count"))
        )
        stmt = self.process_paginate_stmt(stmt, offset, limit)

        result = await self.session.execute(stmt)

        posts = result.all()

        return list(posts)


    async def get_container_posts(
            self, container_id: int,
            offset: int | None = None,
            limit: int | None = None
        ):
        stmt = (
            select(
                *POST_FULL,
            )
            .join(Container, Post.container_id == Container.id)
            .join(User, Post.author_id == User.id)
            .where(Post.container_id == container_id)
        )

        stmt = self.process_paginate_stmt(stmt, offset, limit)


        res = await self.session.execute(stmt)





        print(res.all())







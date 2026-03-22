from base.repository import BaseRepository

from entities import Container, ContainerType, User, Post, Comment

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select


class CommentRepository(BaseRepository[Comment]):

    def __init__(self, session: AsyncSession):
        super().__init__(Comment, session)


    async def get_user_comment_count_in_container(
            self, user_id: int,
            container_type: ContainerType,
            offset: int | None = None,
            limit: int | None = None,
    ) -> list[tuple[Container, int]]:
        # можно потом разные типы контейнеров сделать
        stmt = (
            select(
                Container,
                func.count(Comment.id)
            )
            .join(Post, Post.container_id == Container.id)
            .join(Comment, Comment.post_id == Post.id)
            .where(Comment.author_id == user_id)
            .where(Container.type == container_type)
            .group_by(Container.id)
        )

        stmt = self.process_paginate_stmt(stmt, offset, limit)
        comments = await self.session.execute(stmt)

        return [
            (container, count)
            for container, count in comments.all()
        ]

    def get_full_comment_stmt(self) -> Select:
        return (
            select(Comment, User, Post)
            .join(User, Comment.author_id == User.id)
            .join(Post, Comment.post_id == Post.id)
        )

    async def get_full_comment(self, comment_id: int) -> tuple[Comment, User, Post]:
        stmt = self.get_full_comment_stmt().where(Comment.id == comment_id)

        result = await self.session.execute(stmt)

        return result.one_or_none()

    async def _get_full_comments_from_stmt(
            self, stmt: Select
    ) -> list[tuple[Comment, User, Post]]:

        res = await self.session.execute(stmt)

        return [
            (comment, user, post)
            for comment, user, post in res.all()
        ]

    async def get_post_comments(
            self, post_id: int,
            offset: int | None = None,
            limit: int | None = None
    ) -> list[tuple[Comment, User, Post]]:
        stmt = self.get_full_comment_stmt().where(Comment.post_id ==post_id)
        stmt = self.process_paginate_stmt(stmt, offset, limit)

        return await self._get_full_comments_from_stmt(stmt)



    async def get_user_comments(
            self, user_id: int,
            offset: int | None = None,
            limit: int | None = None
    ) -> list[tuple[Comment, User, Post]]:
        stmt = self.get_full_comment_stmt().filter_by(author_id=user_id)
        stmt = self.process_paginate_stmt(stmt, offset, limit)


        return await self._get_full_comments_from_stmt(stmt)



    async def get_comment_by_id(self, comment_id) -> tuple[Comment, User, Post]:
        stmt = self.get_full_comment_stmt().where(id=comment_id)
        result = await self.session.execute(stmt)

        comment, user, post = result.first()

        return (comment, user, post)









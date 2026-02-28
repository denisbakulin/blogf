from base.repository import BaseRepository
from models.comment import Comment
from models.container import Container, ContainerType
from models.post import Post
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from DTO.comment import CommentDTO, CommentCountInTopic, FullCommentDTO

from sqlalchemy.sql import Select

from models.user import User

from dataclasses import asdict


class CommentRepository(BaseRepository[Comment, CommentDTO]):

    def __init__(self, session: AsyncSession):
        super().__init__(Comment, session, CommentDTO)

    async def create_comment(
            self,
            **comment_data,
    ) -> Comment:
        return self.create(**comment_data)


    async def get_user_comment_count_in_topics(
            self,
            user_id: int,
    ) -> list[CommentCountInTopic]:
        # можно потом разные типы контейнеров сделать
        stmt = (
            select(
                Container.slug,
                func.count(Comment.id)
            )
            .join(
                Post, Post.container_id == Container.id
            )
            .join(
                Comment, Comment.post_id == Post.id
            )
            .where(Comment.author_id == user_id)
            .where(Container.type == ContainerType.topic)
            .group_by(Container.id)
            .limit(10)
        )

        result = await self.session.execute(stmt)

        return [
            CommentCountInTopic(topic_slug=slug, count=count)
            for slug, count in result.tuples().all()
        ]

    def get_full_comment_stmt(self) -> Select:
        return (
            select(
                Comment,
                User.username,
                Post.slug
            )
            .join(User, Comment.author_id == User.id)
            .join(Post, Comment.post_id == Post.id)
        )

    async def _get_comments(self, stmt: Select) -> list[FullCommentDTO]:
        res = await self.session.execute(stmt)

        return [
            FullCommentDTO(**asdict(comment), author_username=author, post_slug=post)
            for comment, author, post in res.all()
        ]

    async def get_post_comments(
            self, post_id: int,
            offset: int | None = None,
            limit: int | None = None
    ) -> list[FullCommentDTO]:
        stmt = self.get_full_comment_stmt().where(post_id=post_id)
        stmt = self.process_paginate_stmt(stmt, offset, limit)
        return await self._get_comments(stmt)

    async def get_user_comments(
            self, user_id: int,
            offset: int | None = None,
            limit: int | None = None
    ) -> list[FullCommentDTO]:
        stmt = self.get_full_comment_stmt().where(user_id=user_id)
        stmt = self.process_paginate_stmt(stmt, offset, limit)
        return await self._get_comments(stmt)

    async def get_comment_by_id(self, comment_id) -> FullCommentDTO:
        stmt = self.get_full_comment_stmt().where(id=comment_id)
        res = await self.session.execute(stmt)

        comment, author, post = res.first()
        return FullCommentDTO(**asdict(comment), author_username=author, post_slug=post)








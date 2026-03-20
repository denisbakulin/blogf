from base.exceptions import EntityBadRequestError
from base.service import BaseService
from entities.comment import Comment
from entities.container import ContainerType
from helpers.search import Pagination
from repositories.comment import CommentRepository
from schemas.comment import CommentCreate, CommentUpdate
from sqlalchemy.ext.asyncio import AsyncSession


class CommentService(BaseService[Comment, CommentRepository]):

    def __init__(self, session: AsyncSession):
        super().__init__(Comment, session, CommentRepository)


    async def create_comment(
            self,
            create: CommentCreate,
            user_id: int,
            post_id: int
    ) -> Comment:
        if create.parent_id is not None:
            parent = await self.get_comment_by_id(create.parent_id)
            if parent.post_id != post_id:
                raise EntityBadRequestError(
                    "Comment",
                    "Родителький комментарий не принадлежит указанному посту"
                )

        comment = await self.create_item(
            **create.model_dump(),
            author_id=user_id, post_id=post_id,
        )

        return comment

    async def update_comment(
            self,
            comment_id: int,
            update: CommentUpdate,
    ) -> Comment:

        return await self.update_item(comment_id, **update.model_dump())



    async def get_comment_by_id(self, comment_id: int) -> Comment:
        return await self.get_item_by_id(comment_id)


    async def get_post_comments(self, post_id: int, pagination: Pagination) -> list:
        return await self.repository.get_post_comments(post_id=post_id, **pagination.dict())


    async def get_user_comments(self, user_id: int, pagination: Pagination) -> list:
        return await self.repository.get_user_comments(user_id=user_id, **pagination.dict())

    async def get_top_themes_of_user(
            self, user_id: int
    ):

        return await self.repository.get_user_comment_count_in_container(
            user_id, container_type=ContainerType.TOPIC
        )
















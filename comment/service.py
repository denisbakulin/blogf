from sqlalchemy.ext.asyncio import AsyncSession
from comment.schemas import CommentCreate, CommentUpdate
from comment.model import Comment
from comment.repository import CommentRepository
from user.service import UserService
from post.service import PostService
from core.exceptions import EntityBadRequestError
from helpers.search import Pagination
from core.service import BaseService
from user.model import User
from post.model import Post

class CommentService(BaseService[Comment]):

    def __init__(self, session: AsyncSession):
        super().__init__(Comment, session, CommentRepository)
        self.user_service = UserService(session=session)
        self.post_service = PostService(session=session)


    async def create_comment(
            self,
            comment_data: CommentCreate,
            user: User,
            post: Post
    ) -> Comment:

        if comment_data.parent_id is not None:
            parent = await self.get_comment_by_id(comment_data.parent_id)
            if parent.post_id != post.id:
                raise EntityBadRequestError(
                    "Comment",
                    "Родителький комментарий не принадлежит указанному посту"
                )

        comment = await self.create_item(
            **comment_data.model_dump(exclude_none=True),
            user_id=user.id, post_id=post.id,
        )

        return comment

    async def update_comment(
            self,
            comment: Comment,
            user: User,
            update_data: CommentUpdate
    ) -> Comment:
        if comment.user_id != user.id:
            raise EntityBadRequestError(
                "Comment",
                f"Комментарий id={comment.id} не принадлежит user={user.username}"
            )

        await self.update_item(comment, **update_data.model_dump())

        return comment

    async def get_comment_by_id(self, comment_id: int) -> Comment:
        return await self.get_item_by_id(comment_id)

    async def get_post_comments(self, post: Post, pagination: Pagination) -> list[Comment]:
        return await self.repository.get_any_by(post_id=post.id, **pagination.get())

    async def get_user_comments(self, user: User, pagination: Pagination) -> list[Comment]:
        return await self.repository.get_any_by(user_id=user.id, **pagination.get())

















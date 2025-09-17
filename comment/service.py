from sqlalchemy.ext.asyncio import AsyncSession
from comment.schemas import CommentCreate
from comment.models import Comment
from comment.repository import CommentRepository
from user.service import UserService
from post.service import PostService


class CommentService:

    def __init__(self, session: AsyncSession):
        self.session = session
        self.comment_repo = CommentRepository(session=session)
        self.user_service = UserService(session=session)
        self.post_service = PostService(session=session)


    async def create_comment(
            self,
            comment_data: CommentCreate,
            author_id: int,
            post_id: int,
            parent_id: int,

    ) -> Comment:

        await self.user_service.get_user_by_id(author_id)
        post = await self.post_service.get_post_by_id(post_id)
        parent = await self.get_comment_by_id(parent_id)

        if parent is None:
            raise
        return await self.comment_repo.create_comment(
            comment_data.model_dump(),
            author_id=author_id,
            post_id=post_id,
            parent_id=parent_id
        )

    async def get_comment_by_id(self, comment_id: int) -> Comment | None:
        return await self.session.get(Comment, comment_id)











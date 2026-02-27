from base.exceptions import EntityBadRequestError
from base.service import BaseService
from helpers.search import Pagination
from models.comment import Comment
from models.post import Post
from repositories.comment import CommentRepository
from schemas.comment import CommentCreate, CommentUpdate
from schemas.topic import UserCommentsCountOfTopicShow
from services.post import PostService
from services.user import UserService
from sqlalchemy.ext.asyncio import AsyncSession
from models.user import User


class CommentService(BaseService[Comment, CommentRepository]):

    def __init__(self, session: AsyncSession):
        super().__init__(Comment, session, CommentRepository)
        self.user_service = UserService(session=session)
        self.post_service = PostService(session=session)



    async def create_comment(
            self,
            comment_create: CommentCreate,
            user: User,
            post: Post
    ) -> Comment:
        if not post.allow_comments:
            raise EntityBadRequestError(
                "Comment",
                f"Под постом [{post.slug}] нельзя оставлять комментарии"
            )

        if comment_create.parent_id is not None:
            parent = await self.get_comment_by_id(comment_create.parent_id)
            if parent.post_id != post.id:
                raise EntityBadRequestError(
                    "Comment",
                    "Родителький комментарий не принадлежит указанному посту"
                )

        comment = await self.create_item(
            **comment_create.model_dump(exclude_none=True),
            author_id=user.id, post_id=post.id,
        )

        return comment

    async def update_comment(
            self,
            comment: Comment,
            comment_update: CommentUpdate,
            user: User,
    ) -> Comment:

        if comment.user_id != user.id:
            raise EntityBadRequestError(
                "Comment",
                f"Комментарий id={comment.id} не принадлежит user={user.username}"
            )

        await self.update_item(comment, **comment_update.model_dump())

        return comment

    async def get_comment_by_id(self, comment_id: int) -> Comment:
        return await self.get_item_by_id(comment_id)

    async def get_post_comments(self, post_id: int, pagination: Pagination) -> list[Comment]:
        return await self.repository.get_any_by(post_id=post_id, **pagination.dict())

    async def get_user_comments(self, user_id: int, pagination: Pagination) -> list[Comment]:
        return await self.repository.get_any_by(user_id=user_id, **pagination.dict())


    async def get_top_themes_of_user(
            self,
            user_id: int
    ) -> list[UserCommentsCountOfTopicShow]:
        top_themes = await self.repository.get_user_comment_count_in_topics(user_id)
        return [
            UserCommentsCountOfTopicShow(topic=topic, count=count)
            for topic, count in top_themes
        ]















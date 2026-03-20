from abac.comment.policy import CommentPolicy
from entities import User
from helpers.search import Pagination
from schemas.comment import CommentCreate, CommentUpdate
from services.comment import CommentService
from services.container import AsyncSession, ContainerService
from services.post import PostService
from services.subscribe import SubscribeService


class BaseCommentUseCase:
    def __init__(
            self,
            session: AsyncSession
    ):
        self.comment_service = CommentService(session)
        self.container_service = ContainerService(session)
        self.post_service = PostService(session)
        self.sub_service = SubscribeService(session)
        self.policy = CommentPolicy(self.sub_service)


class CreateCommentUseCase(BaseCommentUseCase):

    async def execute(self, user: User, create: CommentCreate, post_slug: str):
        post = await self.post_service.get_by_or_raise(slug=post_slug)
        container = await self.container_service.get_item_by_id(post.container_id)

        await self.policy.ensure_create(user=user, container=container)

        comment = await self.comment_service.create_comment(
            create=create, user_id=user.id, post_id=post.id
        )

        await self.container_service.update_item(
            container.id, comment_count=container.comment_count + 1
        )

        return comment


class GetCommentsUseCase(BaseCommentUseCase):
    async def execute(self, user: User, post_slug: str, pagination: Pagination):
        post = await self.post_service.get_by_or_raise(slug=post_slug)
        container = await self.container_service.get_item_by_id(post.container_id)

        await self.policy.ensure_read(user=user, container=container)

        return await self.comment_service.get_post_comments(
            post_id=post.id, pagination=pagination
        )


class UpdateCommentUseCase(BaseCommentUseCase):
    async def execute(self, user: User, comment_id: int, update: CommentUpdate):
        comment = await self.comment_service.get_comment_by_id(comment_id)
        post = await self.post_service.get_item_by_id(comment.post_id)
        container = await self.container_service.get_item_by_id(post.container_id)

        await self.policy.ensure_update(
            user=user, comment=comment, container=container
        )

        return await self.comment_service.update_comment(
            comment_id=comment.id, update=update
        )



class DeleteCommentUseCase(BaseCommentUseCase):
    async def execute(self, user: User, comment_id: int) -> None:
        comment = await self.comment_service.get_comment_by_id(comment_id)
        post = await self.post_service.get_item_by_id(comment.post_id)
        container = await self.container_service.get_item_by_id(post.container_id)

        await self.policy.ensure_delete(
            user=user, comment=comment, container=container
        )

        await self.comment_service.delete_item_by_id(comment.id)

        await self.container_service.update_item(
            container.id, comment_count=container.comment_count - 1
        )

















from abac.post.policy import PostPolicy

from schemas.post import PostCreate, PostUpdate
from services.container import ContainerService, AsyncSession
from services.post import PostService
from services.subscribe import SubscribeService

from entities.user import User
from entities.container import ContainerType
from helpers.search import Pagination



class BasePostUseCase:
    def __init__(
            self,
            session: AsyncSession
    ):
        self.post_service = PostService(session)
        self.container_service = ContainerService(session)
        self.sub_service = SubscribeService(session)
        self.policy = PostPolicy(self.sub_service)


class GetWallPostsUseCase(BasePostUseCase):
    async def execute(self, wall_owner_id: int, pagination: Pagination):
        container = await self.container_service.get_by_or_raise(
            author_id=wall_owner_id, type=ContainerType.wall
        )

        return await self.post_service.get_items_by(
            container_id=container.id, pagination=pagination
        )



class CreatePostUseCase(BasePostUseCase):

    async def execute(self, user: User, post: PostCreate) -> PostCreate:
        container = await self.container_service.get_item_by_id(post.container_id)

        await self.policy.ensure_create(user=user, container=container)


        return await self.post_service.create_post(author_id=user.id, post=post)


class GetPostUseCase(BasePostUseCase):
    async def execute(self, user: User, slug: str):
        post = await self.post_service.get_by_or_raise(slug=slug)
        container = await self.container_service.get_item_by_id(post.container_id)

        await self.policy.ensure_read(user=user, container=container)

        return post


class UpdatePostUseCase(BasePostUseCase):
    async def execute(self, user: User, slug: str, post_update: PostUpdate):
        post = await self.post_service.get_by_or_raise(slug=slug)
        container = await self.container_service.get_item_by_id(post.container_id)

        await self.policy.ensure_update(user=user, post=post, container=container)

        return await self.post_service.update_post(post=post, post_update=post_update)


class DeletePostUseCase(BasePostUseCase):
    async def execute(self, user: User, slug: str) -> None:
        post = await self.post_service.get_by_or_raise(slug=slug)
        container = await self.container_service.get_item_by_id(post.container_id)

        await self.policy.ensure_delete(user=user, post=post, container=container)

        await self.post_service.delete_item_by_id(post.id)

















from abac.post.policy import PostPolicy
from entities import ContainerType, Post, User, Container
from helpers.search import Pagination
from schemas.post import PostCreate, PostUpdate
from services.container import AsyncSession, ContainerService
from services.post import PostService
from services.subscribe import SubscribeService


__all__ = (
    "GetWallPostsUseCase",
    "GetPostsUseCase",
    "CreateWallPostUseCase",
    "CreatePostUseCase",
    "UpdatePostUseCase",
    "DeletePostUseCase",
    "GetPostUseCase"
)

from services.user import UserService


class BasePostUseCase:
    def __init__(
        self, session: AsyncSession
    ):
        self.post_service = PostService(session)
        self.session = session
        self.container_service = ContainerService(session)
        self.sub_service = SubscribeService(session)
        self.policy = PostPolicy(self.session)


class GetWallPostsUseCase(BasePostUseCase):
    async def execute(self, wall_owner_id: int, pagination: Pagination) -> list[Post]:
        container = await self.container_service.get_by_or_raise(
            author_id=wall_owner_id, type=ContainerType.WALL
        )

        return await self.post_service.get_items_by(
            container_id=container.id, pagination=pagination
        )

class GetPostsUseCase(BasePostUseCase):
    async def execute(self, container_id: int, pagination: Pagination, user: User) -> list[tuple[Post, User]]:
        container = await self.container_service.get_item_by_id(container_id)

        await self.policy.ensure_read(user=user, container=container)

        return await self.post_service.get_posts_with_authors(
            container_id=container.id, pagination=pagination
        )



class CreateWallPostUseCase(BasePostUseCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_service = UserService(self.session)


    async def execute(self, user: User, owner_id: int, create: PostCreate) -> Post:
        owner = await self.user_service.get_user_by_id(owner_id)

        wall = await self.container_service.get_by_or_raise(
            author_id=owner.id, type=ContainerType.WALL
        )

        await self.policy.ensure_create(
            user=user, container=wall
        )

        post = await self.post_service.create_post(
            author_id=user.id, post=create, container_id=wall.id
        )

        await self.container_service.update_item(
            wall.id, post_count=wall.post_count + 1
        )

        return post



class CreatePostUseCase(BasePostUseCase):

    async def execute(self, user: User, post: PostCreate, container_id: int) -> Post:
        container = await self.container_service.get_item_by_id(container_id)

        await self.policy.ensure_create(user=user, container=container)

        post = await self.post_service.create_post(
            author_id=user.id, post=post, container_id=container.id
        )

        await self.container_service.update_item(
            container.id, post_count=container.post_count + 1
        )

        return post


class GetPostUseCase(BasePostUseCase):
    async def execute(self, user: User, post_id: int) -> tuple[Post, Container]:
        post = await self.post_service.get_item_by_id(post_id)
        container = await self.container_service.get_item_by_id(post.container_id)

        await self.policy.ensure_read(user=user, container=container)

        return (post, container)



class UpdatePostUseCase(BasePostUseCase):
    async def execute(self, user: User, post_id: int, update: PostUpdate) -> Post:
        post = await self.post_service.get_item_by_id(post_id)
        container = await self.container_service.get_item_by_id(post.container_id)

        await self.policy.ensure_update(user=user, post=post, container=container)

        return await self.post_service.update_post(post_id=post.id, update=update)


class DeletePostUseCase(BasePostUseCase):
    async def execute(self, user: User, post_id: int) -> None:
        post = await self.post_service.get_item_by_id(post_id)
        container = await self.container_service.get_item_by_id(post.container_id)

        await self.policy.ensure_delete(user=user, post=post, container=container)


        await self.post_service.delete_item_by_id(post.id)

        await self.container_service.update_item(
            container.id, post_count=container.post_count - 1
        )
















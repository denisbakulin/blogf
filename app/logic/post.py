from abac.post.policy import PostPolicy

from schemas.post import PostCreate, PostUpdate
from services.container import ContainerService
from services.post import PostService
from services.subscribe import SubscribeService

from DTO.post import PostDTO
from DTO.user import UserDTO



class BasePostUseCase:
    def __init__(
            self,
            post_service: PostService,
            container_service: ContainerService,
            sub_service: SubscribeService,
    ):
        self.post_service = post_service
        self.container_service = container_service
        self.sub_service = sub_service
        self.policy = PostPolicy(self.sub_service)


class CreatePostUseCase(BasePostUseCase):

    async def execute(self, user: UserDTO, post: PostCreate) -> PostCreate:
        container = await self.container_service.get_item_by_id(post.container_id)

        await self.policy.ensure_create(user=user, container=container)


        return await self.post_service.create_post(author_id=user.id, post=post)


class GetPostUseCase(BasePostUseCase):
    async def execute(self, user: UserDTO, slug: str) -> PostDTO:
        post = await self.post_service.get_by_or_raise(slug=slug)
        container = await self.container_service.get_item_by_id(post.container_id)

        await self.policy.ensure_read(user=user, container=container)

        return post


class UpdatePostUseCase(BasePostUseCase):
    async def execute(self, user: UserDTO, slug: str, post_update: PostUpdate):
        post = await self.post_service.get_by_or_raise(slug=slug)
        container = await self.container_service.get_item_by_id(post.container_id)

        await self.policy.ensure_update(user=user, post=post, container=container)

        return await self.post_service.update_post(post=post, post_update=post_update)


class DeletePostUseCase(BasePostUseCase):
    async def execute(self, user: UserDTO, slug: str) -> None:
        post = await self.post_service.get_by_or_raise(slug=slug)
        container = await self.container_service.get_item_by_id(post.container_id)

        await self.policy.ensure_delete(user=user, post=post, container=container)

        await self.post_service.delete_item_by_id(post.id)


class SearchPostUseCase(BasePostUseCase):
    async def execute(self, user: UserDTO, ):
        ...


class GetContainerPostUseCase(BasePostUseCase):
    ...


















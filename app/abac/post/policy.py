from abac.access_level import AccessLevel
from abac.context import ContextResolver
from abac.policy import BasePolicy
from services.subscribe import SubscribeService

from DTO.user import UserDTO
from DTO.container import ContainerDTO
from DTO.post import PostDTO


class PostPolicy:

    def __init__(self, sub_service: SubscribeService):
        self.sub_service = sub_service


    async def ensure_create(self, user: UserDTO, container: ContainerDTO):
        ctx = await ContextResolver(self.sub_service).resolve(user=user, container=container)
        BasePolicy(ctx).ensure_ge_role(AccessLevel.MEMBER)


    async def ensure_update(self, user: UserDTO, post: PostDTO, container: ContainerDTO):
        ctx = await ContextResolver(self.sub_service).resolve(
            user=user, container=container, is_owner=post.author_id == user.id
        )
        BasePolicy(ctx).ensure_ge_role(AccessLevel.OWNER)

    async def ensure_read(self, user: UserDTO, container: ContainerDTO):
        ctx = await ContextResolver(self.sub_service).resolve(
            user=user, container=container
        )
        BasePolicy(ctx).ensure_ge_role(AccessLevel.VIEWER)


    async def ensure_delete(self, user: UserDTO, post: PostDTO, container: ContainerDTO):
        ctx = await ContextResolver(self.sub_service).resolve(
            user=user, container=container, is_owner=post.author_id == user.id
        )
        BasePolicy(ctx).ensure_ge_role(AccessLevel.OWNER)









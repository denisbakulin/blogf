from abac.access_level import AccessLevel
from abac.context import ContextResolver
from abac.policy import BasePolicy
from services.subscribe import SubscribeService

from entities.user import User
from entities.post import Post
from entities.container import Container


class PostPolicy:

    def __init__(self, sub_service: SubscribeService):
        self.sub_service = sub_service


    async def ensure_create(self, user: User, container: Container):
        ctx = await ContextResolver(self.sub_service).resolve(user=user, container=container)
        BasePolicy(ctx).ensure_ge_role(AccessLevel.MEMBER)


    async def ensure_update(self, user: User, post: Post, container: Container):
        ctx = await ContextResolver(self.sub_service).resolve(
            user=user, container=container, is_owner=post.author_id == user.id
        )
        BasePolicy(ctx).ensure_ge_role(AccessLevel.OWNER)

    async def ensure_read(self, user: User, container: Container):
        ctx = await ContextResolver(self.sub_service).resolve(
            user=user, container=container
        )
        BasePolicy(ctx).ensure_ge_role(AccessLevel.VIEWER)


    async def ensure_delete(self, user: User, post: Post, container: Container):
        ctx = await ContextResolver(self.sub_service).resolve(
            user=user, container=container, is_owner=post.author_id == user.id
        )
        BasePolicy(ctx).ensure_ge_role(AccessLevel.OWNER)









from abac.access_level import AccessLevel
from abac.context_resolver import ContextResolver
from abac.policy import BasePolicy, ContextEnsure
from entities.container import Container
from entities.post import Post
from entities.user import User



class PostPolicy(BasePolicy):


    async def ensure_create(self, user: User, container: Container):
        ctx = await self.resolver.resolve(
            user=user, container=container
        )
        ContextEnsure(ctx).ge_role(AccessLevel.MEMBER)


    async def ensure_update(self, user: User, post: Post, container: Container):
        ctx = await self.resolver.resolve(
            user=user, container=container, entity=post
        )
        ContextEnsure(ctx).ge_role(AccessLevel.OWNER)


    async def ensure_read(self, user: User, container: Container):
        ctx = await self.resolver.resolve(
            user=user, container=container
        )
        ContextEnsure(ctx).ge_role(AccessLevel.VIEWER)


    async def ensure_delete(self, user: User, post: Post, container: Container):
        ctx = await self.resolver.resolve(
            user=user, container=container, entity=post
        )
        ContextEnsure(ctx).ge_role(AccessLevel.OWNER)









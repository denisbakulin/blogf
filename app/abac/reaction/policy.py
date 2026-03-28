from abac.access_level import AccessLevel
from abac.context_resolver import ContextResolver
from abac.policy import BasePolicy, ContextEnsure
from entities import Container, Reaction, User, Post
from services.subscribe import SubscribeService


class ReactionPolicy(BasePolicy):

    async def ensure_create(self, user: User, container: Container, post: Post):
        ctx = await self.resolver.resolve(
            user=user, container=container
        )
        ContextEnsure(ctx).ge_role(AccessLevel.VIEWER)
        ContextEnsure.ensure(post.allow_reactions, "Не поддерживаются реакции")


    async def ensure_update(self, user: User, reaction: Reaction, container: Container):
        ctx = await self.resolver.resolve(
            user=user, container=container, entity=reaction
        )
        ContextEnsure(ctx).ge_role(AccessLevel.OWNER)

    async def ensure_read(self, user: User, container: Container):
        ctx = await self.resolver.resolve(
            user=user, container=container
        )
        ContextEnsure(ctx).ge_role(AccessLevel.VIEWER)


    async def ensure_delete(self, user: User, reaction: Reaction, container: Container):
        ctx = self.resolver.resolve(
            user=user, container=container, entity=reaction
        )
        ContextEnsure(ctx).ge_role(AccessLevel.OWNER)










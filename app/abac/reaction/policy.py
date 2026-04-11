from abac.access_level import AccessLevel
from abac.policy import BasePolicy, ContextEnsure
from entities import Container, Reaction, User, Post, ContainerType


class ReactionPolicy(BasePolicy):
    local_rules = False

    async def ensure_create(self, user: User, container: Container, post: Post):
        # Реакции под постом разрешены
        ContextEnsure.ensure(post.allow_reactions, "Не поддерживаются реакции")

        ctx = await self.resolver.resolve(
            user=user, container=container
        )
        ContextEnsure(ctx).ge_role(AccessLevel.VIEWER)



    async def ensure_update(self, user: User, reaction: Reaction, container: Container):
        ctx = await self.resolver.resolve(
            user=user, container=container, entity=reaction
        )
        ContextEnsure(ctx).ge_role(AccessLevel.ENTITY_OWNER)

    async def ensure_read(self, user: User, container: Container):
        # Подробный просмотр реакций только в топике или на стене
        ContextEnsure.ensure(container.type in [
            ContainerType.TOPIC, ContainerType.WALL
        ])

        ctx = await self.resolver.resolve(
            user=user, container=container
        )

        ContextEnsure(ctx).ge_role(AccessLevel.VIEWER)




    async def ensure_delete(self, user: User, reaction: Reaction, container: Container):
        ctx = self.resolver.resolve(
            user=user, container=container, entity=reaction
        )
        ContextEnsure(ctx).ge_role(AccessLevel.ENTITY_OWNER)










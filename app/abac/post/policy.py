from abac.access_level import AccessLevel
from abac.policy import BasePolicy, ContextEnsure
from entities import Post, User, Container
from services.allow import AllowAction, DBEntity, InsufficientAllows

from base.exceptions import check_at_least_one_func_not_raise

class PostPolicy(BasePolicy):


    async def ensure_create(self, user: User, container: Container):
        ctx = await self.resolver.resolve(
            user=user, container=container
        )

        # Если участник контейнера или есть право на создание
        options = [
            (
                lambda: ContextEnsure(ctx).ge_role(AccessLevel.MEMBER),
                InsufficientAllows
            ),
            (
                self.allow.check_access(
                    **ctx.get_dict(),
                    action=AllowAction.CREATE,
                    entity=DBEntity.POST,
                ),
                InsufficientAllows
            )
        ]

        await check_at_least_one_func_not_raise(options)





    async def ensure_update(self, user: User, post: Post, container: Container):
        ctx = await self.resolver.resolve(
            user=user, container=container, entity=post
        )
        ContextEnsure(ctx).ge_role(AccessLevel.ENTITY_OWNER)


    async def ensure_read(self, user: User, container: Container):
        ctx = await self.resolver.resolve(
            user=user, container=container
        )
        ContextEnsure(ctx).ge_role(AccessLevel.VIEWER)


    async def ensure_delete(self, user: User, post: Post, container: Container):
        ctx = await self.resolver.resolve(
            user=user, container=container, entity=post
        )
        ContextEnsure(ctx).ge_role(AccessLevel.ENTITY_OWNER)










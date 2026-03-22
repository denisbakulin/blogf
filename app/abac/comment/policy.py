from abac.access_level import AccessLevel
from abac.context_resolver import ContextResolver
from abac.policy import BasePolicy, ContextEnsure
from entities.comment import Comment
from entities.container import Container
from entities.user import User


class CommentPolicy(BasePolicy):

    async def ensure_create(self, user: User, container: Container):
        ctx = await ContextResolver(self.sub_service).resolve(
            user=user, container=container
        )
        ContextEnsure(ctx).ge_role(AccessLevel.VIEWER)


    async def ensure_update(self, user: User, comment: Comment, container: Container):
        ctx = await ContextResolver(self.sub_service).resolve(
            user=user, container=container, entity=comment
        )
        ContextEnsure(ctx).ge_role(AccessLevel.OWNER)

    async def ensure_read(self, user: User, container: Container):
        ctx = await ContextResolver(self.sub_service).resolve(
            user=user, container=container
        )
        ContextEnsure(ctx).ge_role(AccessLevel.VIEWER)


    async def ensure_delete(self, user: User, comment: Comment, container: Container):
        ctx = await ContextResolver(self.sub_service).resolve(
            user=user, container=container, entity=comment
        )
        ContextEnsure(ctx).ge_role(AccessLevel.OWNER)

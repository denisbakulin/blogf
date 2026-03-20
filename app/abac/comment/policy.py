from abac.access_level import AccessLevel
from abac.context import ContextResolver
from abac.policy import BasePolicy
from entities.comment import Comment
from entities.container import Container
from entities.user import User
from services.subscribe import SubscribeService


class CommentPolicy:

    def __init__(self, sub_service: SubscribeService):
        self.sub_service = sub_service


    async def ensure_create(self, user: User, container: Container):
        ctx = await ContextResolver(self.sub_service).resolve(
            user=user, container=container
        )
        BasePolicy(ctx).ensure_ge_role(AccessLevel.VIEWER)


    async def ensure_update(self, user: User, comment: Comment, container: Container):
        ctx = await ContextResolver(self.sub_service).resolve(
            user=user, container=container, is_owner=comment.author_id == user.id
        )
        BasePolicy(ctx).ensure_ge_role(AccessLevel.OWNER)

    async def ensure_read(self, user: User, container: Container):
        ctx = await ContextResolver(self.sub_service).resolve(
            user=user, container=container
        )
        BasePolicy(ctx).ensure_ge_role(AccessLevel.VIEWER)


    async def ensure_delete(self, user: User, comment: Comment, container: Container):
        ctx = await ContextResolver(self.sub_service).resolve(
            user=user, container=container, is_owner=comment.author_id == user.id
        )
        BasePolicy(ctx).ensure_ge_role(AccessLevel.OWNER)

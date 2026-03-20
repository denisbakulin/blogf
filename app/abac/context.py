
from abac.access import AccessResolver
from abac.access_level import AccessLevel
from entities.container import Container, ContainerType
from entities.user import User
from services.subscribe import SubscribeService

from .data import AccessContext, AuthContext, Context


class ContainerContexBuilder:
    def __init__(self, sub_service: SubscribeService):
        self.sub_service = sub_service

    async def build(self, user, container, is_owner) -> Context:
        raise NotImplementedError()


def ctx_from_access(access: AccessContext, level: AccessLevel) -> Context:
    return Context(
        **access.__dict__, level=level
    )


class PublicChannelContextBuilder(ContainerContexBuilder):
    async def build(self, user: User, container: Container, is_owner: bool) -> Context:
        access_ctx = AccessContext(auth=AuthContext(user_id=user.id), is_owner=is_owner)
        level = await AccessResolver().resolve(
            user=user, context=access_ctx, container=container
        )
        if level is AccessLevel.NONE:
            is_member = await self.sub_service.is_subscriber(
                user_id=user.id, container_id=container.id
            )
            level = AccessLevel.MEMBER if is_member else AccessLevel.VIEWER


        return ctx_from_access(access_ctx, level)


class PrivateChannelContextBuilder(ContainerContexBuilder):
    async def build(self, user: User, container: Container, is_owner: bool) -> Context:
        access_ctx = AccessContext(auth=AuthContext(user_id=user.id), is_owner=is_owner)
        level = await AccessResolver().resolve(
            user=user, context=access_ctx, container=container
        )
        if level is AccessLevel.NONE:
            is_member = await self.sub_service.is_subscriber(
                user_id=user.id, container_id=container.id
            )
            level = AccessLevel.VIEWER if is_member else AccessLevel.NONE

        return ctx_from_access(access_ctx, level)

class TopicContextBuilder(ContainerContexBuilder):
    async def build(self, user: User, container: Container, is_owner: bool) -> Context:
        access_ctx = AccessContext(auth=AuthContext(user_id=user.id), is_owner=is_owner)
        level = await AccessResolver().resolve(
            user=user, context=access_ctx, container=container
        )
        if level == AccessLevel.NONE:
            level = AccessLevel.VIEWER

        return ctx_from_access(access_ctx, level)


class WallContextBuilder(ContainerContexBuilder):
    async def build(self, user: User, container: Container, is_owner: bool) -> Context:
        access_ctx = AccessContext(auth=AuthContext(user_id=user.id), is_owner=is_owner)
        is_wall_owner = container.author_id == user.id

        level = AccessLevel.ADMIN if is_wall_owner else AccessLevel.VIEWER

        return ctx_from_access(access_ctx, level)


class ContextResolver:
    def __init__(self, sub_service: SubscribeService):
        self.builders: dict[ContainerType, type[ContainerContexBuilder]] = {
            ContainerType.WALL: WallContextBuilder,
            ContainerType.TOPIC: TopicContextBuilder,
            ContainerType.PUBLIC_CHANNEL: PublicChannelContextBuilder,
            ContainerType.PRIVATE_CHANEL: PrivateChannelContextBuilder,
        }
        self.sub_service = sub_service

    async def resolve(self, user: User, container: Container, is_owner: bool = False) -> Context:
        return await self.builders[container.type](self.sub_service).build(
            user=user, container=container, is_owner=is_owner
        )



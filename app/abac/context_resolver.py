from abac.access import AccessResolver
from abac.access_level import AccessLevel
from abac.data import AccessContext, AuthContext, Context
from entities import Container, ContainerType, User
from services.subscribe import SubscribeService
from base.model import OwnedByUserMixin
from abc import ABC, abstractmethod


class ContainerContexBuilder(ABC):
    def __init__(
        self,
        sub_service: SubscribeService,
        container: Container,
        user: User,
        entity: OwnedByUserMixin | None = None
    ):
        self.sub_service = sub_service
        self.user = user
        self.container = container
        self.entity = entity

    @abstractmethod
    async def build(self) -> Context:
        pass

    @property
    async def is_subscriber(self) -> bool:
        return await self.sub_service.is_subscriber(
            user_id=self.user.id, container_id=self.container.id
        )

    @property
    def is_owner(self) -> bool:
        if self.entity is None:
            return False
        return self.user.id == self.entity.author_id



    def get_level(self) -> tuple[AccessContext, AccessLevel]:

        access_ctx = AccessContext(
            auth=AuthContext(user_id=self.user.id), is_owner=self.is_owner
        )

        return access_ctx, AccessResolver.resolve(
            user=self.user, context=access_ctx, container=self.container
        )




def ctx_from_access(access: AccessContext, level: AccessLevel) -> Context:
    return Context(**access.__dict__, level=level)


class PublicChannelContextBuilder(ContainerContexBuilder):
    async def build(self) -> Context:

        access_ctx, level = self.get_level()

        if level is AccessLevel.NONE:

            level = AccessLevel.MEMBER if self.is_subscriber else AccessLevel.VIEWER


        return ctx_from_access(access_ctx, level)


class PrivateChannelContextBuilder(ContainerContexBuilder):
    async def build(self) -> Context:
        access_ctx, level = self.get_level()

        if level is AccessLevel.NONE:

            level = AccessLevel.VIEWER if self.is_subscriber else AccessLevel.NONE

        return ctx_from_access(access_ctx, level)


class TopicContextBuilder(ContainerContexBuilder):
    async def build(self) -> Context:
        access_ctx, level = self.get_level()

        if level == AccessLevel.NONE:

            level = AccessLevel.MEMBER if self.is_subscriber else AccessLevel.VIEWER

        return ctx_from_access(access_ctx, level)


class WallContextBuilder(ContainerContexBuilder):
    async def build(self) -> Context:
        access_ctx, level = self.get_level()

        level = AccessLevel.ADMIN if level == AccessLevel.ADMIN else AccessLevel.VIEWER

        return ctx_from_access(access_ctx, level)


class ContextResolver:
    def __init__(self, sub_service: SubscribeService):
        self.sub_service = sub_service

        self.builders: dict[ContainerType, type[ContainerContexBuilder]] = {
            ContainerType.WALL: WallContextBuilder,
            ContainerType.TOPIC: TopicContextBuilder,
            ContainerType.PUBLIC_CHANNEL: PublicChannelContextBuilder,
            ContainerType.PRIVATE_CHANEL: PrivateChannelContextBuilder,
        }


    async def resolve(
        self, user: User,
        container: Container,
        entity: OwnedByUserMixin | None = None
    ) -> Context:

        builder = self.builders[container.type](
            self.sub_service, user=user, container=container, entity=entity
        )

        return await builder.build()



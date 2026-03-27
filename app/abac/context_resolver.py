from sqlalchemy.ext.asyncio import AsyncSession

from abac.access import AccessResolver
from abac.access_level import AccessLevel
from abac.data import AccessContext, AuthContext, Context
from entities import Container, ContainerType, User
from services.admin import AdminService
from services.subscribe import SubscribeService
from base.model import OwnedByUserMixin
from abc import ABC, abstractmethod


class ContainerContexBuilder(ABC):
    def __init__(
        self,
        session: AsyncSession,
        container: Container,
        user: User,
        entity: OwnedByUserMixin | None = None
    ):

        self.user = user
        self.container = container
        self.entity = entity
        self.session = session
        self.subscribe = SubscribeService(session)
        self.admin = AdminService(session)


    @abstractmethod
    async def build(self) -> Context:
        pass


    async def is_subscriber(self) -> bool:
        return await self.subscribe.is_subscriber(
            user_id=self.user.id, container_id=self.container.id
        )

    async def is_admin(self):
        return await self.admin.repository.exists(
            container_id=self.container.id, user_id=self.user.id
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
        is_admin = await self.is_admin()

        if level is AccessLevel.UNDEFINED:
            level = AccessLevel.VIEWER

        if is_admin:
            level = AccessLevel.ADMIN

        return ctx_from_access(access_ctx, level)


class PrivateChannelContextBuilder(ContainerContexBuilder):

    async def build(self) -> Context:
        access_ctx, level = self.get_level()

        is_subscriber = await self.is_subscriber()
        is_admin = await self.is_admin()

        if level is AccessLevel.UNDEFINED:
            level = AccessLevel.VIEWER if is_subscriber else AccessLevel.UNDEFINED

        if is_admin:
            level = AccessLevel.ADMIN

        return ctx_from_access(access_ctx, level)


class TopicContextBuilder(ContainerContexBuilder):
    async def build(self) -> Context:
        access_ctx, level = self.get_level()
        is_subscriber = await self.is_subscriber()
        is_admin = await self.is_admin()

        if level == AccessLevel.UNDEFINED:
            level = AccessLevel.MEMBER if is_subscriber else AccessLevel.VIEWER

        return ctx_from_access(access_ctx, level)


class WallContextBuilder(ContainerContexBuilder):
    async def build(self) -> Context:
        access_ctx, level = self.get_level()

        level = AccessLevel.ADMIN if level == AccessLevel.ADMIN else AccessLevel.VIEWER

        return ctx_from_access(access_ctx, level)


class ContextResolver:


    def __init__(self, session: AsyncSession):
        self.session = session
        self.sub_service = SubscribeService(session)

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
            session=self.session, user=user, container=container, entity=entity
        )

        return await builder.build()



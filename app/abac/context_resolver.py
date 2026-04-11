from sqlalchemy.ext.asyncio import AsyncSession

from abac.access import AccessResolver
from abac.access_level import AccessLevel
from abac.data import AccessContext, AuthContext, Context
from entities import Container, ContainerType, User
from services.admin import AdminService
from services.subscribe import SubscribeService
from base.model import OwnedByUserMixin


class ContainerContexBuilder:
    def __init__(
        self,
        session: AsyncSession,
        user: User,
        container: Container,
        entity: OwnedByUserMixin | None = None
    ):
        self.session = session

        self.user = user
        self.container = container
        self.entity = entity

        self.level = AccessLevel.UNDEFINED

        self.subscribe = SubscribeService(session)
        self.admin = AdminService(session)



    async def build(self) -> Context:
        pass


    async def is_subscriber(self) -> bool:
        return await self.subscribe.is_subscriber(
            user_id=self.user.id, container_id=self.container.id
        )

    async def is_admin(self, *, general: bool = False):
        return await self.admin.repository.exists(
            container_id=None if general else self.container.id,
            user_id=self.user.id
        )


    async def set_admin_status(self):
        if await self.is_admin():
            self.level = AccessLevel.CONTAINER_ADMIN
        if await self.is_admin(general=True):
            self.level = AccessLevel.GENERAL_ADMIN


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



def ctx_from_access(access: AccessContext, level: AccessLevel, container_id: int) -> Context:
    return Context(**access.__dict__, level=level, container_id=container_id)


class PublicChannelContextBuilder(ContainerContexBuilder):
    async def build(self) -> Context:
        access_ctx, self.level = self.get_level()

        if self.level is AccessLevel.UNDEFINED:
            self.level = AccessLevel.VIEWER

        await self.set_admin_status()

        return ctx_from_access(access_ctx, self.level, self.container.id)


class PrivateChannelContextBuilder(ContainerContexBuilder):

    async def build(self) -> Context:
        access_ctx, self.level = self.get_level()
        is_subscriber = await self.is_subscriber()

        if self.level is AccessLevel.UNDEFINED:
            self.level = AccessLevel.VIEWER if is_subscriber else AccessLevel.UNDEFINED

        await self.set_admin_status()

        return ctx_from_access(access_ctx, self.level, self.container.id)




class TopicContextBuilder(ContainerContexBuilder):
    async def build(self) -> Context:
        access_ctx, self.level = self.get_level()
        is_subscriber = await self.is_subscriber()

        if self.level == AccessLevel.UNDEFINED:
            self.level = AccessLevel.MEMBER if is_subscriber else AccessLevel.VIEWER

        await self.set_admin_status()

        return ctx_from_access(access_ctx, self.level, self.container.id)


class WallContextBuilder(ContainerContexBuilder):
    async def build(self) -> Context:
        access_ctx, self.level = self.get_level()

        if self.level == AccessLevel.UNDEFINED:
            self.level = AccessLevel.VIEWER
            await self.set_admin_status()

        return ctx_from_access(access_ctx, self.level, self.container.id)


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



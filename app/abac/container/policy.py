from sqlalchemy.ext.asyncio import AsyncSession

from abac.policy import  ContextEnsure, BasePolicy, AccessLevel, Context
from entities.container import Container
from entities.user import User
from abac.context_resolver import (
    PrivateChannelContextBuilder,
    ContainerContexBuilder,
    TopicContextBuilder
)
from services.admin import AdminService


class BaseContainerPolicy:
    """Базовый класс для взаимодействия с Контейнерами"""

    builder: ContainerContexBuilder

    def __init__(
        self,
        session: AsyncSession,
        user: User,
        container: Container,
    ):
        self.user = user
        self.container = container
        self.session = session

    async def get_contex(self) -> Context:
        return await self.builder.build()


    async def ensure_is_admin(self):
        ctx = await self.get_contex()
        ContextEnsure(ctx).ge_role(AccessLevel.ADMIN)

    async def ensure_is_owner(self):
        ContextEnsure.ensure(self.user.id == self.container.author_id, "НЕ Владелец")


class PrivateChannelPolicy(BaseContainerPolicy):
    builder = PrivateChannelContextBuilder

    async def ensure_read(self):
        ctx = await self.get_contex()
        ContextEnsure(ctx).ge_role(AccessLevel.VIEWER)


class TopicPolicy(BaseContainerPolicy):
    builder = TopicContextBuilder

    @staticmethod
    async def ensure_create(session: AsyncSession, user_id: int):
        admin = AdminService(session)
        await admin.get_by_or_raise(user_id=user_id, container_id=None)











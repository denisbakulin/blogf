from sqlalchemy.ext.asyncio import AsyncSession

from abac.policy import  ContextEnsure, BasePolicy, AccessLevel, Context
from entities.container import Container
from entities.user import User
from abac.context_resolver import (
    PrivateChannelContextBuilder,
    ContainerContexBuilder,
    TopicContextBuilder
)

from base.exceptions import check_at_least_one_func_not_raise, InsufficientPermissionsError
from abac.exceptions import InsufficientAllows
from services.allow import AllowService, AllowAction, DBEntity


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
        ContextEnsure(ctx).ge_role(AccessLevel.CONTAINER_ADMIN)


    async def ensure_is_owner(self):
        ContextEnsure.ensure(self.user.id == self.container.author_id, "НЕ Владелец")


class AllowContainerPolicy(BaseContainerPolicy):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class PrivateChannelPolicy(BaseContainerPolicy):
    builder = PrivateChannelContextBuilder

    async def ensure_read(self):
        ctx = await self.get_contex()
        ContextEnsure(ctx).ge_role(AccessLevel.VIEWER)




class TopicPolicy(BaseContainerPolicy):
    builder = TopicContextBuilder


    @staticmethod
    async def ensure_create(session: AsyncSession, user_id: int):
        allow = AllowService(session)

        # Если глобальный админ или есть разрешение на создание топиков
        options = [
            (
                BasePolicy.ensure_is_global_admin(session, user_id=user_id),
                InsufficientPermissionsError
            ),
            (

                allow.check_access(
                    user_id=user_id, action=AllowAction.CREATE,
                    entity=DBEntity.TOPIC
                ),
                InsufficientAllows
            )
        ]

        await check_at_least_one_func_not_raise(options)











from sqlalchemy.ext.asyncio import AsyncSession

from abac.policy import  ContextEnsure, BasePolicy, AccessLevel, Context
from entities.container import Container
from entities.user import User
from abac.context_resolver import PrivateChannelContextBuilder

class BaseContainerPolicy:
    def __init__(self, session: AsyncSession, user: User, container: Container):
        self.builder = PrivateChannelContextBuilder(
            session=session, user=user, container=container
        )
        self.user = user
        self.container = container
        self.session = session

    async def get_contex(self) -> Context:
        return await self.builder.build()

    async def ensure_is_admin(self):
        ctx = await self.get_contex()
        ContextEnsure(ctx).ge_role(AccessLevel.ADMIN)

    async def ensure_is_owner(self):
        ContextEnsure._ensure(
            self.user.id == self.container.author_id,
            "НЕ Владелец"
        )


class PrivateChannelPolicy(BaseContainerPolicy):

    async def ensure_read(self):
        ctx = await self.get_contex()
        ContextEnsure(ctx).ge_role(AccessLevel.VIEWER)











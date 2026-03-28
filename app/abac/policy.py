from sqlalchemy.ext.asyncio import AsyncSession

from abac.access_level import AccessLevel
from abac.context_resolver import ContextResolver, Context
from abac.exceptions import Forbidden
from abc import ABC, abstractmethod


class BasePolicy(ABC):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.resolver = ContextResolver(self.session)


    @abstractmethod
    async def ensure_read(self, *args, **kwargs): ...

    @abstractmethod
    async def ensure_create(self, *args, **kwargs): ...

    async def ensure_delete(self, *args, **kwargs): ...

    async def ensure_update(self, *args, **kwargs): ...





class ContextEnsure:
    def __init__(self, ctx: Context):
        self.ctx = ctx

    @staticmethod
    def ensure(condition: bool, msg: str | None = None):
        if condition:
            return None
        raise Forbidden(msg)

    def is_owner(self):
        self.ensure(self.ctx.is_owner)

    def ge_role(self, role: AccessLevel):
        self.ensure(self.ctx.level.value >= role.value)





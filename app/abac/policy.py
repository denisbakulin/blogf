from abac.access_level import AccessLevel
from abac.context_resolver import  ContextResolver, Context
from abac.exceptions import Forbidden
from services.subscribe import SubscribeService
from abc import ABC, abstractmethod


class BasePolicy(ABC):
    def __init__(self, sub_service: SubscribeService):
        self.sub_service = sub_service
        self.resolver = ContextResolver(self.sub_service)


    @abstractmethod
    async def ensure_read(self, *args, **kwargs): ...

    @abstractmethod
    async def ensure_create(self, *args, **kwargs): ...

    @abstractmethod
    async def ensure_delete(self, *args, **kwargs): ...

    @abstractmethod
    async def ensure_update(self, *args, **kwargs): ...





class ContextEnsure:
    def __init__(self, ctx: Context):
        self.ctx = ctx

    @staticmethod
    def _ensure(condition: bool, msg: str | None = None):
        if condition:
            return None
        raise Forbidden(msg)

    def is_owner(self):
        self._ensure(self.ctx.is_owner)

    def ge_role(self, role: AccessLevel):
        self._ensure(self.ctx.level.value >= role.value)





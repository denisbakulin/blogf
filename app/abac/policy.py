from sqlalchemy.ext.asyncio import AsyncSession

from abac.access_level import AccessLevel
from abac.context_resolver import ContextResolver, Context
from abac.exceptions import InsufficientAllows
from abc import ABC, abstractmethod
from services.allow import AllowService
from base.exceptions import EntityNotFoundError

from services.admin import AdminService

from base.exceptions import InsufficientPermissionsError



class BasePolicy(ABC):

    # Создание AllowService для проверки локальных правил сущности
    local_rules: bool = True

    def __init__(self, session: AsyncSession):
        self.session = session
        self.resolver = ContextResolver(self.session)
        self.allow = None

        if self.local_rules:
            self.allow = AllowService(self.session)


    @abstractmethod
    async def ensure_read(self, *args, **kwargs): ...

    @abstractmethod
    async def ensure_create(self, *args, **kwargs): ...

    async def ensure_delete(self, *args, **kwargs): ...

    async def ensure_update(self, *args, **kwargs): ...

    @staticmethod
    async def ensure_is_global_admin(session: AsyncSession, user_id: int):
        admin = AdminService(session)
        try:
            await admin.get_by_or_raise(user_id=user_id, container_id=None)
        except EntityNotFoundError as e:
            raise InsufficientPermissionsError("Not a global admin!") from e



class ContextEnsure:
    def __init__(self, ctx: Context):
        self.ctx = ctx

    @staticmethod
    def ensure(condition: bool, msg: str | None = None):
        if condition:
            return None
        raise InsufficientAllows(msg)

    def is_owner(self):
        self.ensure(self.ctx.is_owner)

    def ge_role(self, role: AccessLevel):
        self.ensure(self.ctx.level.value >= role.value)





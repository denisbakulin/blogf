from abac.access_level import AccessLevel
from abac.context import Context
from abac.exceptions import Forbidden


class BasePolicy:
    def __init__(self, ctx: Context):
        self.ctx = ctx

    def _ensure(self, condition: bool):
        if condition:
            return None
        raise Forbidden()

    def ensure_is_owner(self):
        self._ensure(self.ctx.is_owner)

    def ensure_ge_role(self, role: AccessLevel):
        self._ensure(self.ctx.level.value >= role.value)





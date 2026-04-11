from dataclasses import dataclass
from entities import Container
from abac.access_level import AccessLevel


@dataclass
class AuthContext:
    user_id: int


@dataclass
class AccessContext:
    auth: AuthContext
    is_owner: bool


@dataclass
class Context(AccessContext):
    level: AccessLevel
    container_id: int | None = None

    def get_dict(self):
        return {"user_id": self.auth.user_id, "container_id": self.container_id}




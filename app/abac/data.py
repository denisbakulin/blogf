from dataclasses import dataclass

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
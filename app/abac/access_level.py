from enum import Enum, auto


class AccessLevel(Enum):
    NONE = auto()
    BANNED = auto()
    VIEWER = auto()
    MEMBER = auto()
    OWNER = auto()
    ADMIN = auto()



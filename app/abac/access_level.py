from enum import Enum, auto


class AccessLevel(Enum):
    UNDEFINED = auto()
    BANNED = auto()
    VIEWER = auto()
    MEMBER = auto()
    OWNER = auto()
    ADMIN = auto()



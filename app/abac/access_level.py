from enum import Enum, auto


class AccessLevel(Enum):

    UNDEFINED = auto()
    BANNED = auto()
    VIEWER = auto()
    MEMBER = auto()
    ENTITY_OWNER = auto()
    CONTAINER_ADMIN = auto()
    CONTAINER_OWNER = auto()
    GENERAL_ADMIN = auto()



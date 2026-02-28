from dataclasses import dataclass
from enum import StrEnum
from base.DTO import IdMixinDTO, TimeMixinDTO
from DTO.user import UserShortInfo

class ContainerType(StrEnum):
    wall = "wall"
    topic = "topic"
    public_channel = "public_channel"
    private_channel = "private_channel"


@dataclass
class ContainerShortInfo:
    slug: str


@dataclass
class ContainerDTO(IdMixinDTO, TimeMixinDTO):
    type: ContainerType
    title: str
    slug: str
    description: str | None

    author_id: int


@dataclass
class ContainerWithAuthorDTO(ContainerDTO):
    author: UserShortInfo



@dataclass
class MetricsContainerDTO:
    container: ContainerWithAuthorDTO
    post_count: int
    comment_count: int

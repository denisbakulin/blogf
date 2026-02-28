from dataclasses import dataclass
from base.DTO import IdMixinDTO, TimeMixinDTO
from DTO.user import UserShortInfo
from DTO.container import ContainerShortInfo


@dataclass
class PostShortInfo(IdMixinDTO, TimeMixinDTO):
    slug: str


@dataclass
class PostDTO(IdMixinDTO, TimeMixinDTO):
    slug: str
    title: str
    content: str

    allow_comments: bool
    allow_reactions: bool

    container_id: int
    author_id: int


@dataclass
class FullPostDTO(PostDTO):
    container: ContainerShortInfo
    author: UserShortInfo





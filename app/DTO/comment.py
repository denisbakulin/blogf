from dataclasses import dataclass
from base.DTO import IdMixinDTO, TimeMixinDTO
from DTO.user import UserShortInfo
from DTO.container import ContainerShortInfo


@dataclass
class CommentDTO(IdMixinDTO, TimeMixinDTO):
    content: str
    author_id: int
    post_id: int
    parent_id: int | None


@dataclass
class CommentCountInTopic:
    topic_slug: str
    count: int


@dataclass
class FullCommentDTO(CommentDTO):
    author: UserShortInfo
    post: ContainerShortInfo




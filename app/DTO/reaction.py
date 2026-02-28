from enum import StrEnum
from dataclasses import dataclass
from base.DTO import IdMixinDTO, TimeMixinDTO
from DTO.user import UserShortInfo
from DTO.container import ContainerShortInfo
from DTO.post import PostShortInfo

class ReactionType(StrEnum):
    LIKE = "LIKE"
    DISLIKE = "DISLIKE"


@dataclass
class ReactionDTO(IdMixinDTO, TimeMixinDTO):
    user_id: int
    post_id: int | None
    container_id: int | None



@dataclass
class FullReactionDTO(ReactionDTO):
    user: UserShortInfo
    post_id: PostShortInfo | None
    container: ContainerShortInfo | None



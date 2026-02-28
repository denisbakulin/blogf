from dataclasses import dataclass
from base.DTO import IdMixinDTO, TimeMixinDTO
from DTO.user import UserShortInfo
from DTO.container import ContainerShortInfo


@dataclass
class SubscribeDTO(IdMixinDTO, TimeMixinDTO):
    user_id: int
    container_id: int

@dataclass
class FullCommentDTO(SubscribeDTO):
    user: UserShortInfo
    container: ContainerShortInfo



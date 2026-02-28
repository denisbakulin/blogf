from dataclasses import dataclass
from base.DTO import IdMixinDTO, TimeMixinDTO
from models.topic_offer import TopicOfferStatus
from DTO.user import UserShortInfo
from DTO.container import ContainerShortInfo

@dataclass
class TopicOfferDTO(IdMixinDTO, TimeMixinDTO):
    title: str
    description: str
    status: TopicOfferStatus

    author_id: int
    process_user_id: int | None
    release_topic_id: int | None

@dataclass
class FullTopicOfferDTO(TopicOfferDTO):
    author: UserShortInfo
    process_user: UserShortInfo | None
    release_topic: ContainerShortInfo





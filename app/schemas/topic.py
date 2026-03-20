from base.schemas import BaseSchema
from entities.topic_offer import TopicOfferStatus
from schemas.container import ContainerMetricsShow
from schemas.user import UserUsername

class TopicBase(BaseSchema):
    title: str
    description: str


class CreateTopic(TopicBase):
    slug: str


class AddTopicByOffer(BaseSchema):
    status: TopicOfferStatus
    title: str | None = None
    description: str | None = None
    slug: str


class UserCommentsCountOfTopicShow(BaseSchema):
    topic_slug: str
    count: int

class TopicShow(ContainerMetricsShow):
    author: UserUsername
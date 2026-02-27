from base.schemas import BaseSchema
from models.topic_offer import TopicOfferStatus


class TopicBase(BaseSchema):
    title: str
    description: str | None = None


class CreateTopic(TopicBase):
    slug: str


class AddTopicByOffer(BaseSchema):
    status: TopicOfferStatus
    title: str | None = None
    description: str | None = None
    slug: str


class UserCommentsCountOfTopicShow(BaseSchema):
    topic: TopicBase
    count: int

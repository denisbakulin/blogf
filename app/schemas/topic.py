from base.schemas import BaseSchema
from entities.topic_offer import TopicOfferStatus


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
    topic_slug: str
    count: int

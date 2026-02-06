from base.schemas import BaseSchema, IdMixinSchema
from topic.offrer.model import TopicOfferStatus
from user.schemas import UserUsername


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
    count: int

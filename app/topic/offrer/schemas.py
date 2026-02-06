from base.schemas import IdMixinSchema
from topic.offrer.model import TopicOfferStatus
from user.schemas import UserUsername
from topic.release.schemas import TopicBase


class CreateTopicOffer(TopicBase):
    ...


class TopicOfferShow(CreateTopicOffer, IdMixinSchema):
    status: TopicOfferStatus
    author: UserUsername
    process_user: UserUsername | None
    release_topic: TopicBase | None




from base.schemas import IdMixinSchema
from topic.offrer.model import TopicOfferStatus
from topic.release.schemas import TopicBase
from user.schemas import ShortUserInfo


class CreateTopicOffer(TopicBase):
    ...


class TopicOfferShow(CreateTopicOffer, IdMixinSchema):
    status: TopicOfferStatus
    author: ShortUserInfo
    process_user: ShortUserInfo | None
    release_topic: TopicBase | None




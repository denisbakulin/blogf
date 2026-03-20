from base.schemas import IdMixinSchema
from entities.topic_offer import TopicOfferStatus
from schemas.topic import TopicBase
from schemas.user import UserUsername


class CreateTopicOffer(TopicBase):
    pass

class TopicOfferShow(CreateTopicOffer, IdMixinSchema):
    status: TopicOfferStatus


class TopicOfferFullShow(TopicOfferShow):
    author: UserUsername
    process_user: UserUsername | None



from base.schemas import IdMixinSchema
from models.topic_offer import TopicOfferStatus
from schemas.topic import TopicBase
from schemas.user import UserUsername



class CreateTopicOffer(TopicBase):
    ...


class TopicOfferShow(CreateTopicOffer, IdMixinSchema):
    status: TopicOfferStatus
    author: UserUsername
    process_user: UserUsername| None


